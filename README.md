# Moving Average Crossover Backtest

This project implements a simple moving average (SMA) crossover backtesting strategy for Gold price data.

## Strategy Overview

-   **Short SMA**: 5-period average of the closing price.
-   **Long SMA**: 20-period average of the closing price.
-   **Signal**:
    -   `1` (Long) when Short SMA > Long SMA.
    -   `0` (Flat) otherwise.
-   **Execution**: Signals are shifted by one period (position_t = signal_{t-1}) to avoid lookahead bias.
-   **Trade Size**: Fixed at $100 per trade.

## Files

-   [`backtest.py`](backtest.py): The main Python script to run the crossover backtest.
-   [`backtest_explanation.md`](backtest_explanation.md): Detailed breakdown of the project logic and results explanation.
-   [`15_June_months.csv`](15_June_months.csv): 15-minute interval Gold price data.
-   [`30_June_months.csv`](30_June_months.csv): 30-minute interval Gold price data.

## Setup

1.  Ensure you have Python installed.
2.  Install the required libraries:
    ```bash
    pip install pandas numpy
    ```
3.  Run the backtest:
    ```bash
    python backtest.py
    ```

## Results Summary

The backtest merges the 15-minute and 30-minute data files into a single timeline. Typical results show the total number of trades, asset cumulative return, strategy cumulative return, and total profit in USD.

See `backtest_explanation.md` for a deeper analysis of why the strategy performs the way it does.
