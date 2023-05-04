import matplotlib.pyplot as plt


def plot_operations(operaciones, price,
                    parcial=True,
                    sides='BOTH',
                    column_price_df_price='c',
                    column_time_open='time_open', column_time_close='time_close',
                    column_side='side',
                    long='LONG', short='SHORT',
                    column_price_open='price_open', column_price_close='price_close',
                    column_time_close_parcial='time_close_parcial', column_price_close_parcial='price_close_parcial', ):
    """
    Plotea el precio con las operaciones
    Precio como una linea
    operaciones:
    - Entrada LONG como una ^ verde
    - Salida LONG como una v verde
    - Salida LONG TP como un - verde
    - Entrada SHORT como una v roja
    - Salida SHORT como una ^ roja
    - Salida SHORT TP como un - rojo


    Necesito:
    - Precio del ticker
    - Fecha de inicio de operacion
    - Side
    - Fecha de salida parcial
    - Fecha de salida total

    :return:
    """
    pass

    # price = price.iloc[-10000:].copy()

    sides = [long, short] if sides == 'BOTH' else [sides]

    # Comienza el ploteo
    plt.style.use('dark_background')
    # plt.figure(figsize=(40, 16))
    plt.figure(figsize=(20, 8))

    # Plot Price
    f1 = plt.plot(price[column_price_df_price])

    # Plot others
    if long in sides:
        # opens
        df_plot = operaciones[operaciones[column_side] == long].copy()
        df_plot.index = df_plot[column_time_open]

        price['plot_' + column_time_open] = df_plot[column_price_open].copy() * 0.98
        plt.plot(price.index, price['plot_' + column_time_open], marker='^', color='green')

        # closes
        df_plot.index = df_plot[column_time_close]

        price['plot_' + column_time_close] = df_plot[column_price_close].copy() * 1.02
        plt.plot(price.index, price['plot_' + column_time_close], marker='v', color='green')

        if parcial:
            # df_plot[column_time_close_parcial] sin False
            df_plot_parcial = df_plot[df_plot[column_time_close_parcial] != False].copy()
            df_plot_parcial.index = df_plot_parcial[column_time_close_parcial]

            price['plot_' + column_time_close_parcial] = df_plot_parcial[column_price_close_parcial].copy() * 1.02
            plt.plot(price.index, price['plot_' + column_time_close_parcial], marker='*', color='green')

    if short in sides:
        # opens
        df_plot = operaciones[operaciones[column_side] == short].copy()
        df_plot.index = df_plot[column_time_open]

        price['plot_' + column_time_open] = df_plot[column_price_open].copy() * 1.02
        plt.plot(price.index, price['plot_' + column_time_open], marker='v', color='red')

        # closes
        df_plot.index = df_plot[column_time_close]

        price['plot_' + column_time_close] = df_plot[column_price_close].copy() * 0.98
        plt.plot(price.index, price['plot_' + column_time_close], marker='^', color='red')

        if parcial:
            # df_plot[column_time_close_parcial] sin False
            df_plot_parcial = df_plot[df_plot[column_time_close_parcial] != False].copy()
            df_plot_parcial.index = df_plot_parcial[column_time_close_parcial]

            price['plot_' + column_time_close_parcial] = df_plot_parcial[column_price_close_parcial].copy() * 0.98
            plt.plot(price.index, price['plot_' + column_time_close_parcial], marker='*', color='red')

    plt.legend(f1, ['Price'])
    plt.grid(which='major', axis='y', color='white', lw=1, alpha=0.15)
    plt.minorticks_on()
    plt.grid(which='minor', axis='both', color='white', lw=1, alpha=0.15)
    plt.suptitle(f'Operaciones', y=0.92)

    # plt.show()
    return plt


def add_ma(plt, ma_fast, ma_slow):

    plt.plot(ma_fast, color='yellow')
    plt.plot(ma_slow, color='orange')

    return plt
