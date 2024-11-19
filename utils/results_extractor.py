from datetime import datetime, timedelta
import re

def extract_data(data_string):
    # Define keys and their expected data types
    keys_map = {
        "Start": "datetime",
        "End": "datetime",
        "Duration": "timedelta",
        "Exposure Time [%]": "float",
        "Equity Final [$]": "float",
        "Equity Peak [$]": "float",
        "Return [%]": "float",
        "Buy & Hold Return [%]": "float",
        "Return (Ann.) [%]": "float",
        "Volatility (Ann.) [%]": "float",
        "Sharpe Ratio": "float",
        "Sortino Ratio": "float",
        "Calmar Ratio": "float",
        "Max. Drawdown [%]": "float",
        "Avg. Drawdown [%]": "float",
        "Max. Drawdown Duration": "timedelta",
        "Avg. Drawdown Duration": "timedelta",
        "# Trades": "int",
        "Win Rate [%]": "float",
        "Best Trade [%]": "float",
        "Worst Trade [%]": "float",
        "Avg. Trade [%]": "float",
        "Max. Trade Duration": "timedelta",
        "Avg. Trade Duration": "timedelta",
        "Profit Factor": "float",
        "Expectancy [%]": "float",
        "SQN": "float",
        "Kelly Criterion": "float",
        "_strategy": "string",
        "_equity_curve": "string",
        "_trades": "string",        
    }

    data_dict = {}

    for line in data_string.strip().split('\n'):
        # Split by two or more spaces to ensure proper key-value separation
        parts = re.split(r' {2,}', line.strip())
        if len(parts) == 2:
            key, value = parts
            if key in keys_map:
                data_type = keys_map[key]
                
                # Parse value based on the data type
                if data_type == "datetime":
                    data_dict[key] = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                elif data_type == "timedelta":
                    days, _, time = value.partition(' days ')
                    if time == '':
                        data_dict[key] = timedelta(days=int(days))
                    else:
                        hours, minutes, seconds = map(int, time.split(':'))
                        data_dict[key] = timedelta(days=int(days), hours=hours, minutes=minutes, seconds=seconds)
                elif data_type == "float":
                    data_dict[key] = float(value.strip('%$'))
                elif data_type == "int":
                    data_dict[key] = int(value)
                elif data_type == "string":
                    data_dict[key] = value
            else:
                print(f"Warning: Unexpected key '{key}' found. Skipping...")

    return data_dict
