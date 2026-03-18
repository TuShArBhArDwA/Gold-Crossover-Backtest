import os
import glob
import pandas as pd
import numpy as np

# setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TRADE_SIZE = 100 
SHORT_WINDOW = 5
LONG_WINDOW = 20

# load csvs
csv_files = glob.glob(os.path.join(SCRIPT_DIR, "*.csv"))
if not csv_files:
    raise FileNotFoundError("no csv files found in the folder.")

frames = [pd.read_csv(p, parse_dates=["start_time"]) for p in csv_files]
data = pd.concat(frames, ignore_index=True).sort_values("start_time").reset_index(drop=True)

print(f"loaded {len(data)} rows")

# calculate moving averages
data["SMA_short"] = data["close"].rolling(SHORT_WINDOW).mean()
data["SMA_long"] = data["close"].rolling(LONG_WINDOW).mean()

# signals (1 for long, 0 for flat)
data["signal"] = np.where(data["SMA_short"] > data["SMA_long"], 1, 0)

# shift by 1 to avoid lookahead bias
data["position"] = data["signal"].shift(1).fillna(0)

# returns
data["daily_return"] = data["close"].pct_change()
data["strategy_return"] = data["position"] * data["daily_return"]

# cumulative returns
data["cum_asset_return"] = (1 + data["daily_return"]).cumprod() - 1
data["cum_strategy_return"] = (1 + data["strategy_return"]).cumprod() - 1

# trades and profit
data["trade_entry"] = (data["position"].diff() == 1).astype(int)
data["pnl_usd"] = data["strategy_return"] * TRADE_SIZE

# save output
output_cols = [
    "start_time", "close", "SMA_short", "SMA_long",
    "signal", "position", "daily_return", "strategy_return",
    "cum_asset_return", "cum_strategy_return", "trade_entry", "pnl_usd"
]
result = data[output_cols].copy()
out_path = os.path.join(SCRIPT_DIR, "backtest_results.csv")
result.to_csv(out_path, index=False)

# summary metrics
valid = result.dropna(subset=["strategy_return"])
num_trades = int(valid["trade_entry"].sum())
total_asset_ret = valid["cum_asset_return"].iloc[-1] * 100
total_strat_ret = valid["cum_strategy_return"].iloc[-1] * 100

print("\n--- results ---")
print(f"trades: {num_trades}")
print(f"asset return: {total_asset_ret:.2f}%")
print(f"strategy return: {total_strat_ret:.2f}%")
print(f"total profit (USD): ${valid['pnl_usd'].sum():.2f}")