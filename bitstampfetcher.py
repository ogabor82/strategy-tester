import json
import requests
import pandas as pd
import datetime


currency_pair = "btcusd"
url = f"https://www.bitstamp.net/api/v2/ohlc/{currency_pair}/"

# start = "2021-01-01"
# end = "2022-01-01"

start = "2011-08-01"
end = "2025-01-22"

dates = pd.date_range(start, end, freq="165D", inclusive="both")
if dates[-1] != pd.to_datetime(end):
    dates = dates.append(pd.DatetimeIndex([pd.to_datetime(end)]))


dates = [int(x.value / 10**9) for x in list(dates)]

# print(dates)
for date in dates:
    print(datetime.datetime.fromtimestamp(date))

master_data = []

for first, last in zip(dates, dates[1:]):
    print(datetime.datetime.fromtimestamp(first), datetime.datetime.fromtimestamp(last))

    params = {
        "step": 14400,  # 4 hours
        "limit": 1000,
        "start": first,
        "end": last,
    }

    data = requests.get(url, params=params)

    data = data.json()["data"]["ohlc"]

    master_data += data

df = pd.DataFrame(master_data)
df = df.drop_duplicates()

df["timestamp"] = df["timestamp"].astype(int)
df = df.sort_values(by="timestamp")

df = df[df["timestamp"] >= dates[0]]
# df = df[df["timestamp"] < dates[-1]]

df["datetime"] = pd.to_datetime(df["timestamp"], unit="s")

print(df)

df.to_csv("ohlc/bitstamp.btc.4h.csv", index=False)
