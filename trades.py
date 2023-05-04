import numpy as np
import pandas as pd


def add_signal_rsi(data, rsi_buy, rsi_sell):

    return np.where(data['rsi'] < rsi_buy, 'LONG', np.where(data['rsi'] > rsi_sell, 'SHORT', ''))


def add_signal_close_rsi(data, rsi_close=50, column_rsi='rsi', column_signal_rsi='signal_rsi'):

    # Le agrego la columna close si el rsi cruza hacia arriba o hacia abajo el rsi_close
    close = data[
        ((data[column_rsi] < rsi_close) & (data[column_rsi].shift() > rsi_close)) |
        ((data[column_rsi] > rsi_close) & (data[column_rsi].shift() < rsi_close))
    ].copy()
    close['close_position'] = 'close'

    # concat close_position with data
    data = data.copy()
    data = pd.concat([data, close['close_position']], axis=1)

    # concat long_short with close_position
    data[column_signal_rsi] = np.where(data['close_position'] == 'close', 'close', data[column_signal_rsi])
    return data[column_signal_rsi]


def make_trades_rsi(data, rsi_buy=30, rsi_sell=70, tendencia=False, column_cruce='cruce_ema'):
    """
    Tendencia, si es True, toma el cruce de medias para habilitar los trades dependiendo de la tendencia
    :param rsi_sell:
    :param rsi_buy:
    :param column_cruce:
    :param data:
    :param tendencia:
    :return:
    """

    data = data.copy()

    # add signal
    data['signal_rsi'] = add_signal_rsi(data, rsi_buy, rsi_sell)
    data['signal_rsi'] = add_signal_close_rsi(data)

    # drop rows where long_short is none
    data = data[data['signal_rsi'] != '']

    if tendencia:
        # change values cruce_ema, if cruce_ema > 0 == 'LONG, else 'SHORT'
        data[column_cruce] = np.where(data[column_cruce] > 0, 'LONG', 'SHORT')

        # drop when signal_rsi is different to cruce_ema or close
        data = data[(data['signal_rsi'] == data[column_cruce]) | (data['signal_rsi'] == 'close')]

    # keep first short and first long
    data = data[data['signal_rsi'].shift(1) != data['signal_rsi']]

    # delete first row if signal_rsi is close
    data = data.iloc[1:] if data.iloc[0]['signal_rsi'] == 'close' else data

    # delte last row if long_short != close
    data = data.iloc[:-1] if data.iloc[-1]['signal_rsi'] != 'close' else data

    # Seteo los precios open y close, y las fechas de date_open y date_close
    data['open'] = data['close']
    data['close'] = data['close'].shift(-1)
    data.index.names = ['date']
    data.reset_index(inplace=True)
    data['date_open'] = data['date']
    data['date_close'] = data['date'].shift(-1)

    # delete rows close
    data = data[data['signal_rsi'] != 'close']

    # make results
    data['result'] = np.where(data['signal_rsi'] == 'long', data['close'] / data['open'] - 1, data['open'] / data['close'] - 1)
    data['result_acumulado'] = ((data['result'] + 1).cumprod() - 1)

    data.drop(['high', 'low', 'date', 'volume', 'rsi', 'cruce_ema'], axis=1, inplace=True)
    data.dropna(inplace=True)

    return data


