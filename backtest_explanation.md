# Backtest Explanation: Moving Average Crossover

Here is exactly what the code did in the background to generate those numbers:

### 1. Data Combination
The script loaded both `15_June_months.csv` and `30_June_months.csv`, merged them into a single continuous timeline, and sorted them by time. That's why it printed `loaded 32565 rows`.

### 2. Moving Average Calculations 
On every single row, the script calculated two trailing averages of the `close` price:
- **Short SMA**: Average of the last 5 closing prices
- **Long SMA**: Average of the last 20 closing prices

### 3. Generating the Signal (The Crossover)
For each row, it checked: *Is the 5-bar SMA higher than the 20-bar SMA?*
- If **Yes**, the signal becomes `1` (buy/hold).
- If **No**, the signal becomes `0` (flat/out of market).

### 4. Taking Positions (Avoiding Lookahead Bias)
To ensure the backtest is realistic, it shifts the signal forward by one row. This means if the crossover happens *at the current bar's close*, the script enters the trade at the start of the *next* bar.

### 5. Calculating Returns
It then calculated how much the price changed from bar to bar. 
- **Asset Return**: If you just bought at the very beginning of the data and held until the end, your return was `39.86%`. 
- **Strategy Return**: Whenever the strategy's position was `1`, it multiplied that bar's return by 1. Whenever it was `0`, the return for that bar was 0. 

### Why did the strategy underperform the asset? (2.03% vs 39.86%)

1. **Trades: 1136**. The crossovers happened *very* frequently (likely because gold is choppy and you combined 15m and 30m data). Entering and exiting 1,136 times means the strategy constantly got chopped up by false signals (whipsaws) where the short SMA crossed the long SMA, but no actual trend followed.
2. **Missing the Up-Trends**: Because moving averages are lagging indicators, by the time the 5-bar SMA crossed the 20-bar SMA to get you into the trade, a large part of the price movement had already occurred. When the price dropped, it stayed in the trade until the 5-bar eventually crossed under the 20-bar, causing it to catch the downside before exiting.
3. **Total Profit**: Because the strategy return was a cumulative 2.03%, and the trade size was set to $100 per entry, the net total profit over those 1.1k chopped-up trades ended up being a very small $2.72. 

**Next Steps**: If you want to improve this, we usually increase the moving average windows (e.g., 20 and 50) so it doesn't trade as often, or ensure we only use one timeframe of data at a time to avoid scrambling the signals.
