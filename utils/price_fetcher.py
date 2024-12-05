from binance.client import Client
import yfinance as yf
import pandas as pd

def fetch_binance_prices(ticker, start_date, end_date, frequency):
    client = Client()
    binance_interval = {
        '1d': Client.KLINE_INTERVAL_1DAY,
        '1h': Client.KLINE_INTERVAL_1HOUR,
        '15m': Client.KLINE_INTERVAL_15MINUTE,
    }[frequency]
    
    klines = client.get_historical_klines(
        ticker, 
        binance_interval,
        start_date,
        end_date
    )
    
    df_prices = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 
        'volume', 'close_time', 'quote_asset_volume',
        'number_of_trades', 'taker_buy_base_asset_volume',
        'taker_buy_quote_asset_volume', 'ignore'
    ])
    df_prices['timestamp'] = pd.to_datetime(df_prices['timestamp'], unit='ms')
    df_prices.set_index('timestamp', inplace=True)
    df_prices = df_prices[['open', 'high', 'low', 'close', 'volume']].astype(float)
    
    # Rename columns to match expected format
    df_prices = df_prices.rename(columns={
        'open': 'Open',
        'high': 'High',
        'low': 'Low',
        'close': 'Close',
        'volume': 'Volume'
    })
    
    return df_prices

def fetch_yahoo_prices(ticker, start_date, end_date, frequency):
    df_prices = yf.Ticker(ticker).history(start=start_date, end=end_date, interval=frequency)
    df_prices.index = df_prices.index.tz_localize(None)
    return df_prices

def get_price_data(ticker, start_date, end_date, frequency):
    # Check if the ticker ends with "USDT"
    if ticker.endswith("USDT"):
        return fetch_binance_prices(ticker, start_date, end_date, frequency)
    else:
        return fetch_yahoo_prices(ticker, start_date, end_date, frequency) 