from binance.client import Client
import yfinance as yf
import pandas as pd


def fetch_binance_prices(ticker, start_date, end_date, frequency):
    client = Client()
    binance_interval = {
        "1d": Client.KLINE_INTERVAL_1DAY,
        "4h": Client.KLINE_INTERVAL_4HOUR,
        "1h": Client.KLINE_INTERVAL_1HOUR,
        "30m": Client.KLINE_INTERVAL_30MINUTE,
        "15m": Client.KLINE_INTERVAL_15MINUTE,
        "5m": Client.KLINE_INTERVAL_5MINUTE,
        "1m": Client.KLINE_INTERVAL_1MINUTE,
    }[frequency]

    klines = client.get_historical_klines(
        ticker, binance_interval, start_date, end_date
    )

    df_prices = pd.DataFrame(
        klines,
        columns=[
            "timestamp",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "quote_asset_volume",
            "number_of_trades",
            "taker_buy_base_asset_volume",
            "taker_buy_quote_asset_volume",
            "ignore",
        ],
    )
    df_prices["timestamp"] = pd.to_datetime(df_prices["timestamp"], unit="ms")
    df_prices.set_index("timestamp", inplace=True)
    df_prices = df_prices[["open", "high", "low", "close", "volume"]].astype(float)

    # Rename columns to match expected format
    df_prices = df_prices.rename(
        columns={
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "volume": "Volume",
        }
    )

    return df_prices


def fetch_yahoo_prices(ticker, start_date, end_date, frequency):
    df_prices = yf.Ticker(ticker).history(
        start=start_date, end=end_date, interval=frequency
    )
    df_prices.index = df_prices.index.tz_localize(None)
    return df_prices


def fetch_bitstamp_prices(ticker, start_date, end_date, frequency):
    # Read the CSV file
    df_prices = pd.read_csv(f"./bitstamp.testall.30min.csv")

    # Convert timestamp to datetime and set as index
    df_prices["timestamp"] = pd.to_datetime(df_prices["timestamp"], unit="s")
    df_prices.set_index("timestamp", inplace=True)

    # Filter by date range
    df_prices = df_prices.loc[start_date:end_date]

    # Resample data to match requested frequency if needed
    if frequency != "30m":
        # Map common frequencies to pandas offset aliases
        freq_map = {
            "1m": "1T",
            "5m": "5T",
            "15m": "15T",
            "1h": "1H",
            "4h": "4H",
            "1d": "1D",
        }

        if frequency in freq_map:
            # For downsampling (e.g., 30m to 1h)
            df_prices = df_prices.resample(freq_map[frequency]).agg(
                {
                    "open": "first",
                    "high": "max",
                    "low": "min",
                    "close": "last",
                    "volume": "sum",
                }
            )

    # Ensure column names match the expected format
    df_prices = df_prices.rename(
        columns={
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "volume": "Volume",
        }
    )

    return df_prices


def get_price_data(ticker, start_date, end_date, frequency):
    # Check if the ticker ends with "USDT"
    if ticker.endswith("USDT") or ticker.endswith("USDC"):
        return fetch_binance_prices(ticker, start_date, end_date, frequency)
    elif ticker.endswith("USD"):
        return fetch_bitstamp_prices(ticker, start_date, end_date, frequency)
    else:
        return fetch_yahoo_prices(ticker, start_date, end_date, frequency)
