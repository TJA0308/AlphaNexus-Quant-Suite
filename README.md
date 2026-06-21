# AlphaNexus Backtesting Lab

AlphaNexus is a backtesting workbench for testing simple long-only trading rules on historical market data. A user chooses a ticker, strategy, date range, starting capital, fee, and slippage assumptions; the app then compares the strategy against buy-and-hold and reports risk and trade-level results.

The project is built to be explainable: the strategies are intentionally simple, while the codebase separates data loading, indicators, signal generation, portfolio simulation, metrics, API responses, and UI rendering.

## What It Demonstrates

- Python analytics with `pandas` and `numpy`
- FastAPI backend with typed request/response models
- Next.js and TypeScript frontend scaffold
- Streamlit dashboard for a quick local demo
- Strategy signal generation for SMA crossover, RSI mean reversion, and Bollinger breakout
- Portfolio simulation with cash, shares, transaction fees, slippage, and benchmark comparison
- Risk metrics including total return, Sharpe ratio, max drawdown, win rate, and completed trade count
- Unit tests for indicators and backtest behavior

## Live Demo

The Streamlit version is the recommended public demo because it runs from a single entry point:

```text
app.py
```

Streamlit Community Cloud settings:

```text
Repository: TJA0308/AlphaNexus-Quant-Suite
Branch: main
Main file path: app.py
```

## Project Structure

```text
.
|-- alphanexus/
|   |-- backtest.py       # Portfolio simulation engine
|   |-- data.py           # Market data loading and normalization
|   |-- indicators.py     # SMA, RSI, Bollinger Bands
|   |-- metrics.py        # Sharpe, drawdown, performance summary
|   `-- strategies.py     # Strategy signal generation
|-- api/
|   `-- main.py           # FastAPI app
|-- frontend/
|   `-- app/              # Next.js TypeScript interface
|-- tests/                # pytest coverage for core logic
|-- app.py                # Streamlit demo interface
|-- requirements.txt
`-- pyproject.toml
```

For a more detailed explanation, see [docs/architecture.md](docs/architecture.md).

## How The Backtest Works

1. Load historical OHLCV data for a ticker.
2. Calculate indicators such as moving averages, RSI, or Bollinger Bands.
3. Convert indicators into long-only buy/sell signals.
4. Shift from signals into executed trades while tracking cash, shares, fees, and slippage.
5. Build an equity curve and buy-and-hold benchmark.
6. Calculate return, drawdown, Sharpe ratio, win rate, and trade-level realized PnL.

The app is a research and education tool. It is not financial advice and it does not predict future returns.

## Assumptions And Limits

- The simulator is long-only: it holds cash or one long position.
- Signals are generated from historical close prices.
- Fees and slippage are applied on executed trades.
- The benchmark is buy-and-hold over the same selected period.
- The strategies are intentionally simple and should not be treated as production trading models.
- Results can change when market data providers revise historical data.

## Local Setup

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Run the Streamlit demo:

```bash
streamlit run app.py
```

Run the FastAPI backend:

```bash
uvicorn api.main:app --reload
```

Open the API docs at:

```text
http://127.0.0.1:8000/docs
```

Run the Next.js frontend:

```bash
cd frontend
cmd /c npm install
cmd /c npm run dev
```

The frontend expects the API at `http://127.0.0.1:8000`. To use another API URL, set:

```bash
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

## Testing

```bash
pytest
```

Current test coverage focuses on:

- Indicator calculation behavior
- Strategy/backtest execution
- Fee handling and non-negative cash behavior
- Trade execution events

## Interview Explanation

> I built a backtesting dashboard to learn how analytics products are structured end to end. The backend fetches market data, computes indicators, generates trading signals, simulates a portfolio with fees and slippage, and returns risk metrics through a FastAPI endpoint. The frontend lets a user configure a strategy and inspect the equity curve, drawdown, benchmark comparison, and trade ledger.

## Resume Bullet

> Built a full-stack financial backtesting dashboard using Python, FastAPI, pandas, NumPy, Next.js, TypeScript, and Streamlit, enabling users to test parameterized trading strategies, compare against buy-and-hold benchmarks, and analyze Sharpe ratio, max drawdown, win rate, and trade-level PnL.

## Next Improvements

- Add saved backtest history with SQLite or DuckDB.
- Add walk-forward testing to reduce overfitting.
- Add portfolio-level multi-asset allocation.
- Add Playwright tests for the Next.js user flow.
- Add Dockerfiles for consistent deployment.
