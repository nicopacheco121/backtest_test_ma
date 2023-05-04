from api_yfinance import yfinance_data
from indicators import add_rsi, add_cruce_ema, add_ema
import pandas as pd
from trades import make_trades_rsi
from plots import plot_operations, add_ma

# # show more columns in pandas
# pd.set_option('display.max_columns', 500)

def run(ma_fast=20, ma_slow=50, ticker='SPY', descargar_data=True, rsi_buy=35, rsi_sell=65, tendencia=True):
    # Data
    if descargar_data:
        data = yfinance_data(ticker=ticker, interval='1d', years_data=20)

        # change column names to lowercase
        data.columns = [x.lower() for x in data.columns]

        data.to_pickle(f'data/{ticker}.pkl')
    else:
        data = pd.read_pickle(f'data/{ticker}.pkl')

    # Agrego indicadores
    data['rsi'] = add_rsi(data)
    data['cruce_ema'] = add_cruce_ema(df_copy=data, k1=ma_fast, k2=ma_slow)

    # delete rsi 0
    data = data[data['rsi'] != 0]

    # Primero, trades solo con el rsi
    trades = make_trades_rsi(data, rsi_buy=rsi_buy, rsi_sell=rsi_sell, tendencia=tendencia)

    # change signal_rsi to signal
    trades = trades.rename(columns={'signal_rsi': 'signal'})

    print(trades)

    plot = plot_operations(operaciones=trades,
                           price=data,
                           parcial=False,
                           sides='BOTH',
                           column_price_df_price='close',
                           column_time_open='date_open',
                           column_time_close='date_close',
                           column_side='signal',
                           column_price_open='open',
                           column_price_close='close',
                           )

    if tendencia:
        # add ma to plot
        data['ma_fast'] = add_ema(data, 'close', ma_fast)
        data['ma_slow'] = add_ema(data, 'close', ma_slow)

        plot = add_ma(plot, ma_fast=data['ma_fast'], ma_slow=data['ma_slow'])

    plot.savefig('plot.png', dpi=300)
    plot.show()



if __name__ == '__main__':
    pass
    run(ticker='SPY', descargar_data=False, tendencia=True)