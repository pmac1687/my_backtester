import pandas as pd
from datetime import datetime


def write_to_csv(obj):
    _date = datetime.now().strftime("%Y-%m-%d")
    df_old = []
    try:
        df_old = pd.read_excel(f"{obj.name}_{_date}.xlsx")
        df_old = df_old.iloc[:, 1:]
    except:
        print(1)
    writer = pd.ExcelWriter(f"{obj.name}_{_date}.xlsx", engine="xlsxwriter")
    columns = [
        "ticker",
        "indicator",
        "long value",
        "long buys",
        "short value",
        "short sells",
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
            df["short_value"][-1],
            df["short_sells"][-1],
            df["param"][-1],
            df.index[0],
            df.index[-1],
            df["Close"].min(),
            df["Close"].max(),
            df["Volume"].min(),
            df["Volume"].max(),
        ]
        data.append(dats)

    df = pd.DataFrame(data, columns=columns)
    print("dfold", type(df_old))
    print("df_new", type(df))
    # print(df_old.tolist())
    if type(df_old) != list:
        # frames = [df, df_old]
        # print("frames", frames)
        # res = pd.concat(frames, axis=1, join_axes=[df_old.index], sort=True)
        # print("res", res)
        # print(df)
        # res.to_excel(writer)
        # print(df_old.values.to_list())
        datas = []
        df_old = df_old.values.tolist()
        print("data", data)
        print("df_old", df_old)
        for i in range(len(data)):
            datas.append(df_old[i])
            datas.append(data[i])
        res = pd.DataFrame(datas, columns=columns)
        res.to_excel(writer)
    else:
        df.to_excel(writer)

    writer.save()


#
## Write your DataFrame to a file
# df.to_excel(writer, "Sheet1")
## Save the result
# writer.save()


if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d"))
    pass
