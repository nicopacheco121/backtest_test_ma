from talipp.indicators import RSI


# add rsi
def add_rsi(data):

    data_dict = data.to_dict('list')
    data_dict = {'open': data_dict['open'], 'high': data_dict['high'], 'low': data_dict['low'], 'close': data_dict['close']}
    list_rsi = list(RSI(period=14, input_values=data_dict['close']))
    # add zeros al principio de la lista ccl
    list_cci = [0] * (len(data) - len(list_rsi)) + list_rsi
    return list_cci


def add_ema(df, column_name, k):
    if k == 0:
        return df[column_name]
    else:
        return df[column_name].ewm(span=k, adjust=False).mean()


def add_cruce_ema(df_copy, k1, k2, column_name='close'):
    df = df_copy.copy()

    if k1 == 0:
        df['media1'] = df[column_name]
    else:
        df['media1'] = add_ema(df, column_name, k1)
    df['media2'] = add_ema(df, column_name, k2)

    return df['media1'] / df['media2'] - 1
