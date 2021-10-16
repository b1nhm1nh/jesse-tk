datadir = 'jessetkdata'

Metrics = {
    'start_date': None,
    'finish_date': None,
    'symbol': None,
    'tf': None,
    'dna': 'None',
    'total_trades': 0,
    'total_profit': 0,
    'max_dd': 0,
    'annual_return': 0,
    'paid_fees': 0,
    'win_rate': 0,
    'n_of_longs': 0,
    'n_of_shorts': 0,
    'serenity': 0,
    'sharpe': 0,
    'calmar': 0,
    'sortino': 0,
    'win_strk': 0,
    'lose_strk': 0,
    'largest_win': 0,
    'largest_lose': 0,
    'n_of_wins': 0,
    'n_of_loses': 0,
    'market_change': 0,
}

csvd = '\t'

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

refine_console_formatter = '{: <12} {: <6} {: <5} {: <7}{: <12} {: <8} {: <10} {: <8} {: <8} {: <8} {: <8} {: <8} {: <8} ' \
                           '{: <12} {: <12} {: <10} {: <8} {: <8} {: <8}'