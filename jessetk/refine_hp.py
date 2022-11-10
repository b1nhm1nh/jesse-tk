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
import arrow
#-----------------------------------------------
#  Refine HP in a time range
#  Additional 


class Refine:
    def __init__(self, hp_filename,  start_date, finish_date, wf_steps: int, wf_inc_month: int, wf_test_month: int, cpu :int, full_reports: bool):

        import signal
        signal.signal(signal.SIGINT, self.signal_handler)

        self.hp_filename = hp_filename

        self.start_date = start_date
        self.finish_date = finish_date

        self.wf_steps = wf_steps
        self.wf_inc_month = wf_inc_month
        self.wf_test_month = wf_test_month
        self.full_reports = full_reports

        self.cpu = cpu

        self.jessetkdir = datadir
        self.anchor = 'DNA!'
        self.sort_by = {'serenity': 12, 'sharpe': 13, 'calmar': 14}

        self.metrics = []

        self.n_of_iters = 0
        self.results = []
        self.sorted_results = []
        self.results_without_dna = []

        self.hps_module = None
        self.routes_template = None
        self.hps = None

        self.n_of_dnas = None

        r = router.routes[0]  # Read first route from routes.py
        self.exchange = r.exchange.replace(' ', '_')
        self.pair = r.symbol
        self.timeframe = r.timeframe
        self.strategy = r.strategy_name

        self.removesimilardnas = False

        self.ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename = f'Refine_hp-{self.exchange}-{self.pair}-{self.timeframe}--{start_date}--{finish_date}'

        self.hp_file_name = f'{self.jessetkdir}/results/{self.filename}--{self.ts}.txt'
        self.report_file_name = f'{self.jessetkdir}/results/{self.filename}--{self.ts}.csv'
        self.log_file_name = f'{self.jessetkdir}/logs/{self.filename}--{self.ts}.log'

    def run(self):
        max_cpu = self.cpu
        processes = []
        commands = []
        results = []
        iters_completed = 0
        # self.hps = self.import_hp()
        self.hps = utils.import_hp_files(self.hp_filename)

        self.n_of_dnas = len(self.hps)
        print(f"Save hp file: {len(self.hps)}")
        self.save_hps_file()

        l_iters = self.n_of_dnas
        index = 0  # TODO Reduce number of vars ...
        start = timer()

        while l_iters > 0:
            commands = []

            for _ in range(max_cpu):
                if l_iters > 0:
                    l_iters -= 1
                    hp = json.loads(self.hps[index])
                    hp['report_prefix'] = str(index)

                    commands.append(
                        f"jesse-tk backtest {self.start_date} {self.finish_date} {'--full-reports' if self.full_reports else ''} --prefix={index} --hp=\"{hp}\" ")
                    index += 1

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

                if metric['sharpe'] is not None and metric not in results:
                    results.append(deepcopy(metric))

                sorted_results_prelist = sorted(results, key=lambda x: 0 if x['sharpe'] is None else float(x['sharpe']), reverse=True)

                self.sorted_results = []


                self.sorted_results = sorted_results_prelist

                clear_console()

                eta = ((timer() - start) / index) * (self.n_of_dnas - index)
                eta_formatted = strftime("%H:%M:%S", gmtime(eta))
                print(
                    f'{index}/{self.n_of_dnas}\teta: {eta_formatted} | {self.pair} '
                    f'| {self.timeframe} | {self.start_date} -> {self.finish_date}')

                self.print_tops_formatted()

        if self.wf_steps > 0:
            for r in self.sorted_results:
                r['sum_sharpe'] = r['sharpe']
            # Walkforward refine
            for step in range(1, self.wf_steps):

                a_start_date = arrow.get(self.finish_date, 'YYYY-MM-DD').shift(months=-self.wf_inc_month * step)
                a_finish_date = a_start_date.shift(months=self.wf_test_month)

                l_iters = self.n_of_dnas
                index = 0  # TODO Reduce number of vars ...
                start = timer()

                while l_iters > 0:
                    commands = []

                    for _ in range(max_cpu):
                        if l_iters > 0:
                            l_iters -= 1
                            hp = json.loads(self.hps[index])
                            hp['report_prefix'] = str(index)

                            commands.append(
                                f"jesse-tk backtest {a_start_date.format('YYYY-MM-DD')} {a_finish_date.format('YYYY-MM-DD')} {'--full-reports' if self.full_reports else ''} --prefix={index} --hp=\"{hp}\" ")
                            index += 1

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

                        if metric['sharpe'] is not None and metric not in results:
                            results.append(deepcopy(metric))

                        
                        for r in self.sorted_results:
                            if r['dna'] == metric['dna']:
                                r['sum_sharpe'] += float(metric['sharpe'])
                                break

                        # sorted_results_prelist = sorted(results, key=lambda x: 0 if x['sum_sharpe'] is None else float(x['sum_sharpe']), reverse=True)
                        # self.sorted_results = []

                        self.sorted_results = sorted(self.sorted_results, key=lambda x: 0 if x['sum_sharpe'] is None else float(x['sum_sharpe']), reverse=True)


                        clear_console()

                        eta = ((timer() - start) / index) * (self.n_of_dnas - index)
                        eta_formatted = strftime("%H:%M:%S", gmtime(eta))
                        print(f'{index}/{self.n_of_dnas}\teta: {eta_formatted} | {self.pair} '
                            f'| {self.timeframe} | {a_start_date.format("YYYY-MM-DD")} -> {a_finish_date.format("YYYY-MM-DD")}  | WF step {step}/{self.wf_steps}')

                        self.print_tops_formatted(step)            

        utils.create_csv_report(self.sorted_results,
                                self.report_file_name, refine_file_header)

    def signal_handler(self, sig, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

    def import_hp(self):
        with open(self.hp_filename, "r") as f:
            hp = f.readlines()
            f.close()
        return hp
 
    # v TODO Move to utils
    def print_tops_formatted(self, step: int = 1):
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
                    round(r['sum_sharpe'] / step,2) if 'sum_sharpe' in r.keys() else r['sharpe'],
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

    def save_hps_file(self,):

        jessetk.utils.remove_file(self.hp_file_name)

        with open(self.hp_file_name, 'w', encoding='utf-8') as f:
            i = 0
            for hp in self.hps:
                f.write(f"{i}\t{hp}\n")
                i += 1
        # f.flush()
        f.close()
        # f.flush()
        # os.fsync(f.fileno())



    def write_dna_file(self, f, sorted_results):
        f.write('dnas = [\n')

        for srr in sorted_results:
            for dnac in self.hps:
                if srr['dna'] == dnac[0]:
                    f.write(str(dnac) + ',\n')

        f.write(']\n')
        f.flush()
        os.fsync(f.fileno())

    def get_config(self, config_file):
        import pathlib
        import yaml

        cfg_file = pathlib.Path(config_file)

        # return loaded config
        if len(self.config_data):
            return self.config_data
            
        if not cfg_file.is_file():
            print(f"{config_file} not found. Run create-config command.")
            exit()
        else:
            with open(config_file, "r") as ymlfile:
                cfg = yaml.load(ymlfile, yaml.SafeLoader)
                self.config_data = cfg
        return cfg