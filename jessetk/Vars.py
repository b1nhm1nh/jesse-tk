datadir = 'jessetkdata'
initial_test_message = 'Please wait while performing initial test...'
csvd = '\t'  # csv delimiter

Metrics = {
    'start_date': None,
    'finish_date': None,
    'exchange': 'None',
    'symbol': None,
    'tf': None,  # timeframe
    'strategy': None,
    'dna': 'None',
    'total_trades': None,
    'total_profit': 0.0,
    'max_dd': 0.0,
    'annual_return': 0.0,
    'paid_fees': 0.0,
    'win_rate': 0,
    'n_of_longs': 0,
    'n_of_shorts': 0,
    'serenity': 0.0,
    'sharpe': None,
    'calmar': None,
    'sortino': None,
    'smart_sharpe': None,
    'smart_sortino': None,
    'win_strk': 0.0,
    'lose_strk': 0.0,
    'largest_win': 0.0,
    'largest_lose': 0.0,
    'n_of_wins': 0,
    'n_of_loses': 0,
    'market_change': 0.0,
    'seq_hps': 'None',
    'parameters': 'None',
}

refine_file_header = ['Pair',
                      'TF',
                      'Dna',
                      'Start Date',
                      'End Date',
                      'Total Trades',
                      'Longs %',
                      'Short %',
                      'Total Net Profit',
                      'Max.DD',
                      'Annual Profit',
                      'Winrate',
                      'Serenity',
                      'Sharpe',
                      'Calmar',
                      'Winning Strike',
                      'Losing Strike',
                      'Largest Winning',
                      'Largest Losing',
                      'Num. of Wins',
                      'Num. of Losses',
                      'Paid Fees',
                      'Market Change']

refine_console_header1 = ['Dna',
                          'Total',
                          'Longs',
                          'Shorts',
                          'Total Net',
                          'Max.',
                          'Annual',
                          'Win',
                          'Serenity',
                          'Sharpe',
                          'Calmar',
                          'Winning',
                          'Losing',
                          'Largest',
                          'Largest',
                          'Winning',
                          'Losing',
                          'Paid',
                          'Market']
refine_console_header2 = ['String',
                          'Trades',
                          '%',
                          '%',
                          'Profit %',
                          'DD %',
                          'Return %',
                          'Rate %',
                          'Index',
                          'Ratio',
                          'Ratio',
                          'Streak',
                          'Streak',
                          'Win. Trade',
                          'Los. Trade',
                          'Trades',
                          'Trades',
                          'Fees',
                          'Change %']
refine3_console_header1 = ['Dna',
                          '_Total',
                          'Max.DD',
                          'Sharpe',
                          'Total Net',
                          'Max.',
                          'Annual',
                          'Win',
                          'Serenity',
                          'Sharpe',
                          'Calmar',
                          'Winning',
                          'Losing',
                          'Largest',
                          'Largest',
                          'Winning',
                          'Losing',
                          'Paid',
                          'Market']
refine3_console_header2 = ['String',
                          'Profit%',
                          '%',
                          '',
                          'Profit %',
                          'DD %',
                          'Return %',
                          'Rate %',
                          'Index',
                          'Ratio',
                          'Ratio',
                          'Streak',
                          'Streak',
                          'Win. Trade',
                          'Los. Trade',
                          'Trades',
                          'Trades',
                          'Fees',
                          'Change %']
refine_console_formatter = '{: <12} {: <6} {: <5} {: <7}{: <12} {: <8} {: <10} {: <8} {: <8} {: <8} {: <8} {: <8} {: <8} ' \
                           '{: <12} {: <12} {: <10} {: <8} {: <8} {: <8}'
refine3_console_formatter = '{: <13} {: <8} {: <6} {: <6} {: <8} {: <8} {: <10} {: <8} {: <8} {: <8} {: <8} {: <8} {: <8} ' \
                           '{: <12} {: <12} {: <10} {: <8} {: <8} {: <8}'


refinewf_console_header1 = ['Dna',
                          'TNP',
                          'Max DD',
                          'Sharpe',
                          '| TNP ',
                          'Max DD',
                          'Annual',
                          'WR',
                          'Serenity',
                          'Sharpe',
                          'Calmar',
                          'Win/Lose',
                          'Win/Lose',
                          'Max',
                          'Max',
                          'Paid']
refinewf_console_header2 = ['String',
                          'Last',
                          'Last',
                          'Last',
                          '|  % ',
                          '  %',
                          'Ret %',
                          '  %',
                          'Index',
                          'Ratio',
                          'Ratio',
                          'Streak',
                          'Trades',
                          'Win',
                          'Loss',
                          'Fees']

refinewf_console_formatter = '{: <26} {: <8} {: <6} {: <6} {: <8} {: <8} {: <10} {: <6} {: <8} {: <8} {: <8} {: <8} ' \
                           '{: <12} {: <12} {: <10} {: <8}'
random_file_header = ['Pair',  # TODO Pairs for multi routes?
                      'TF',
                      'Dna',
                      'Start Date',
                      'End Date',
                      'Total Trades',
                      'Longs %',
                      'Short %',
                      'Total Net Profit',
                      'Max.DD',
                      'Annual Profit',
                      'Winrate',
                      'Serenity',
                      'Sharpe',
                      'Calmar',
                      'Winning Strike',
                      'Losing Strike',
                      'Largest Winning',
                      'Largest Losing',
                      'Num. of Wins',
                      'Num. of Losses',
                      'Paid Fees',
                      'Market Change']

random_console_header1 = ['Start',
                          'End',
                          'Total',
                          'Longs',
                          'Shorts',
                          'Total Net',
                          'Max.',
                          'Annual',
                          'Win',
                          'Serenity',
                          'Sharpe',
                          'Calmar',
                          'Winning',
                          'Losing',
                          'Largest',
                          'Largest',
                          'Winning',
                          'Losing',
                          'Paid',
                          'Market']
random_console_header2 = ['Date',
                          'Date',
                          'Trades',
                          '%',
                          '%',
                          'Profit %',
                          'DD %',
                          'Return %',
                          'Rate %',
                          'Index',
                          'Ratio',
                          'Ratio',
                          'Streak',
                          'Streak',
                          'Win. Trade',
                          'Los. Trade',
                          'Trades',
                          'Trades',
                          'Fees',
                          'Change %']

random_console_formatter = '{: <12} {: <12} {: <6} {: <5} {: <7}{: <12} {: <8} {: <10} {: <8} {: <8} {: <8} {: <8} {: <8} {: <8} ' \
                           '{: <12} {: <12} {: <10} {: <8} {: <8} {: <8}'
