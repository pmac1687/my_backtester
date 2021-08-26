def calculate_portfolio(obj, df, indicator_type):
    """
    loop through df['signals']
    long:
        if df.signals == 1.0 buy long
        when df.signals == -1.0 sell
    short:
        if df.signals == -1.0 sell short 
        when df.signals == 1.0 exit short position
    note:
        only take first df.signal of 1.0, -1.0, 
        maybe series before you reach next sell signal
    indicator_type:: 'stockstats' or 'tapy':
                    indicate if stockstats:'close' or tapy:'Close'
    """
    close_dic = {"tapy": "Close", "stockstats": "close"}
    close = close_dic[indicator_type]
    long_capital = 100000.0
    long_position = 0.0
    in_position = False
    df["long_p-l"] = 0.0
    df["long_positions"] = 0.0
    df["long_capital"] = 0.0
    for i in range(len(df)):
        if (df["signals"][i] == 1.0) and (in_position == False):
            long_position = long_capital / df[close][i]
            in_position = True
        if (df["signals"][i] == -1.0) and (in_position == True):
            new_capital = long_position * df[close][i]
            df["long_p-l"][i] = (long_capital - new_capital) * -1
            long_capital = new_capital
            long_position = 0.0
            in_position = False
        df["long_positions"][i] = long_position
        df["long_capital"][i] = long_capital
    df["long_value"] = sum(df["long_p-l"])
    """
    when selling short, get percent of close price of the day selling
    than take capital from when you bought the short times sell price percent
    """
    short_capital = 100000.0
    short_position = 0.0
    short_price = 0.0
    sell_price = 0.0
    in_position = False
    df["short_positions"] = 0.0
    df["short_capital"] = 0.0
    df["short_p-l"] = 0.0
    df["short_price"] = 0.0
    df["sell_price"] = 0.0
    for b in range(len(df)):
        if (df["signals"][b] == -1.0) and (in_position == False):
            short_position = short_capital / df[close][b]
            short_price = df[close][b]
            in_position = True
            print("neg")
        if (df["signals"][b] == 1.0) and (in_position == True):
            sell_price_percent = short_price / df[close][b]
            df["short_p-l"][b] = (
                short_capital - (short_capital * sell_price_percent)
            ) * -1
            short_capital = short_capital * sell_price_percent
            short_position = 0.0
            sell_price = df[close][b]
            in_position = False
        df["sell_price"][b] = sell_price
        df["short_price"][b] = short_price
        df["short_positions"][b] = short_position
        df["short_capital"][b] = short_capital
    df["short_value"] = sum(df["short_p-l"])
    print(df)


if __name__ == "__main__":
    pass

