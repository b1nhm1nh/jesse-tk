import importlib
import os
import sys
from copy import deepcopy
from datetime import datetime
from subprocess import PIPE, Popen
from time import strftime, gmtime
from timeit import default_timer as timer

from jesse.modes import backtest_mode
from jesse.routes import router
from jesse.services import db
from jesse.services import report

import jessetk.Vars as Vars
import jessetk.utils
from jessetk import utils, print_initial_msg, clear_console
from jessetk.Vars import datadir
from jessetk.Vars import refine_file_header
import json

class Refine:
    def __init__(self, hp_filename,  start_date, finish_date, cpu):

        import signal
        signal.signal(signal.SIGINT, self.signal_handler)

        self.hp_filename = hp_filename

        self.start_date = start_date
        self.finish_date = finish_date
        self.cpu = cpu


        self.jessetkdir = datadir
        self.anchor = 'DNA!'
        self.sort_by = {'serenity': 12, 'sharpe': 13, 'calmar': 14}

        self.metrics = []

        self.n_of_iters = 0
        self.results = []
        self.sorted_results = []
        self.results_without_dna = []

        self.dnas_module = None
        self.routes_template = None
        self.dnas = None

        self.n_of_dnas = None

        r = router.routes[0]  # Read first route from routes.py
        self.exchange = r.exchange.replace(' ', '_')
        self.pair = r.symbol
        self.timeframe = r.timeframe
        self.strategy = r.strategy_name

        self.removesimilardnas = False

        self.ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename = f'Refine_hp-{self.exchange}-{self.pair}-{self.timeframe}--{start_date}--{finish_date}'

        self.report_file_name = f'{self.jessetkdir}/results/{self.filename}--{self.ts}.csv'
        self.log_file_name = f'{self.jessetkdir}/logs/{self.filename}--{self.ts}.log'

    def run(self):
        max_cpu = self.cpu
        processes = []
        commands = []
        results = []
        sorted_results = []
        iters_completed = 0
        self.dnas = self.import_hp()

        self.n_of_dnas = len(self.dnas)
  
        l_iters = self.n_of_dnas

        index = 0  # TODO Reduce number of vars ...
        start = timer()
        print(f"Size of dna: {len(self.dnas)}")

        while l_iters > 0:
            commands = []

            for _ in range(max_cpu):
                if l_iters > 0:
                    l_iters -= 1
                    # print ( self.dnas[l_iters] )
                    hp = json.loads(self.dnas[l_iters])
                    hp['report_prefix'] = str(l_iters)
                    # print (hp)

                    # hp.append()

                    commands.append(
                        f"jesse-tk backtest {self.start_date} {self.finish_date} --full-reports --prefix={l_iters} --hp=\"{hp}\" ")
                    index += 1
            # quit()
            processes = [Popen(cmd, shell=True, stdout=PIPE) for cmd in commands]
            # wait for completion
            for p in processes:
                p.wait()

                # Get thread's console output
                (output, err) = p.communicate()
                # debug
                # print(output.decode('utf-8'))
                # exit()
                iters_completed += 1

                # Map console output to a dict
                metric = utils.get_metrics3(output.decode('utf-8'))

                if metric not in results:
                    results.append(deepcopy(metric))

                sorted_results_prelist = sorted(results, key=lambda x: float(x['sharpe']), reverse=True)

                self.sorted_results = []


                self.sorted_results = sorted_results_prelist

                clear_console()

                eta = ((timer() - start) / index) * (self.n_of_dnas - index)
                eta_formatted = strftime("%H:%M:%S", gmtime(eta))
                print(
                    f'{index}/{self.n_of_dnas}\teta: {eta_formatted} | {self.pair} '
                    f'| {self.timeframe} | {self.start_date} -> {self.finish_date}')

                self.print_tops_formatted()
        utils.create_csv_report(self.sorted_results,
                                self.report_file_name, refine_file_header)
        # if self.eliminate:
        #     self.save_dnas(self.sorted_results, self.dna_py_file)
        # else:
        #     self.save_dnas(self.sorted_results)

        # utils.create_csv_report(self.sorted_results,
        #                         self.report_file_name, refine_file_header)



    def signal_handler(self, sig, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

    def import_hp(self):
        with open(self.hp_filename, "r") as f:
            hp = f.readlines()
            f.close()
        return hp
 
    # v TODO Move to utils
    def print_tops_formatted(self):
        print('\033[1m', end='')
        print(
            Vars.refine_console_formatter.format(*Vars.refine_console_header1))
        print(
            Vars.refine_console_formatter.format(*Vars.refine_console_header2))
        print('\033[0m', end='')

        for r in self.sorted_results[0:25]:
            print(
                Vars.refine_console_formatter.format(
                    r['dna'],
                    r['total_trades'],
                    r['n_of_longs'],
                    r['n_of_shorts'],
                    r['total_profit'],
                    r['max_dd'],
                    r['annual_return'],
                    r['win_rate'],
                    r['serenity'],
                    r['sharpe'],
                    r['calmar'],
                    r['win_strk'],
                    r['lose_strk'],
                    r['largest_win'],
                    r['largest_lose'],
                    r['n_of_wins'],
                    r['n_of_loses'],
                    r['paid_fees'],
                    r['market_change']))

    def save_dnas(self, sorted_results, dna_fn=None):

        if not dna_fn:
            dna_fn = f'{self.jessetkdir}/dnafiles/{self.pair} {self.start_date} {self.finish_date}.py'

        jessetk.utils.remove_file(dna_fn)

        with open(dna_fn, 'w', encoding='utf-8') as f:
            self.write_dna_file(f, sorted_results)

    def write_dna_file(self, f, sorted_results):
        f.write('dnas = [\n')

        for srr in sorted_results:
            for dnac in self.dnas:
                if srr['dna'] == dnac[0]:
                    f.write(str(dnac) + ',\n')

        f.write(']\n')
        f.flush()
        os.fsync(f.fileno())
