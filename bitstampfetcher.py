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

dates = pd.date_range(start, end, freq="20D")
dates = [int(x.value / 10**9) for x in list(dates)]

print(dates)

master_data = []

for first, last in zip(dates, dates[1:]):
    print(first, last)

    params = {
        "step": 1800,  # 1800 = 30 minutes
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
df = df[df["timestamp"] < dates[-1]]

df["datetime"] = pd.to_datetime(df["timestamp"], unit="s")

print(df)

df.to_csv("bitstamp.testall.30min.csv", index=False)
