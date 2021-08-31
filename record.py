import pandas as pd
from datetime import datetime


def write_to_csv(obj):
    """
    we record our result. while looping, if no xlsx exists, we write to file
    if file already exists we read data to memory than copy over in addition
    to data were adding.
    """
    _date = datetime.now().strftime("%Y-%m-%d")
    df_old = []
    close = "Close" if obj.indicator == "tapy" else "close"
    volume = "Volume" if obj.indicator == "tapy" else "volume"
    try:
        df_old = pd.read_excel(f"records/{obj.name}_{_date}.xlsx")
        df_old = df_old.iloc[:, 1:]
    except:
        print("no existing")
    writer = pd.ExcelWriter(f"records/{obj.name}_{_date}.xlsx", engine="xlsxwriter")
    columns = [
        "ticker",
        "indicator",
        "long value",
        "long buys",
        "long avg",
        "long high",
        "long low",
        "short value",
        "short sells",
        "short avg",
        "short high",
        "short low",
        "params",
        "date start",
        "date end",
        "close low",
        "close high",
        "volume low",
        "volume high",
    ]
    data = []
    for df in obj.df_results:
        dats = [
            obj.ticker,
            obj.name,
            df["long_value"][-1],
            df["long_buys"][-1],
            df["avg_buys"][-1],
            df["long_high"][-1],
            df["long_low"][-1],
            df["short_value"][-1],
            df["short_sells"][-1],
            df["avg_sells"][-1],
            df["short_high"][-1],
            df["short_low"][-1],
            df["param"][-1],
            df.index[0],
            df.index[-1],
            df[close].min(),
            df[close].max(),
            df[volume].min(),
            df[volume].max(),
        ]
        data.append(dats)

    df = pd.DataFrame(data, columns=columns)
    if type(df_old) != list:
        datas = []
        df_old = df_old.values.tolist()
        for i in range(len(data)):
            datas.append(df_old[i])
            datas.append(data[i])
        res = pd.DataFrame(datas, columns=columns)
        res.to_excel(writer)
    else:
        df.to_excel(writer)

    writer.save()


if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d"))
    pass
