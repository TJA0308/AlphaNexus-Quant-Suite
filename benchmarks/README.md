# AlphaNexus Benchmarks

This benchmark measures the backtest engine on deterministic fixture data. It intentionally excludes live `yfinance` download time because provider latency, rate limits, and data revisions are outside the simulation engine.

## Scenario Matrix

The current matrix runs:

| Dimension | Count | Values |
| --- | ---: | --- |
| Fixtures | 8 | trend, mean-reversion, volatility, breakout, cycle, flat, shock/recovery regimes |
| Date windows | 3 | full fixture, first half, second half |
| Strategies | 3 | SMA crossover, RSI mean reversion, Bollinger breakout |
| Total scenarios | 72 | 8 fixtures x 3 windows x 3 strategies |

Each scenario loads a cached OHLCV CSV, generates strategy signals, simulates portfolio execution with fees and slippage, and computes risk/performance metrics.

## Run It

```bash
python benchmarks/run_backtest_benchmark.py
```

Optional JSON output:

```bash
python benchmarks/run_backtest_benchmark.py --json
```

Optional p95 guard:

```bash
python benchmarks/run_backtest_benchmark.py --fail-on-p95-ms 100
```

## Example Local Result

Run on Windows with Python 3.13.6:

```text
Scenarios passed: 72/72 (100.0%)
Fixture rows processed: 24,120
Median engine runtime: 13.71 ms
P95 engine runtime: 20.85 ms
Max engine runtime: 33.12 ms
```

These numbers are local machine measurements and can move slightly between runs. The defendable claim is the methodology: deterministic fixtures, fixed scenario matrix, engine-only timing, and a pytest regression test that verifies the same matrix completes successfully.

## Regenerate Fixtures

```bash
python benchmarks/generate_fixtures.py
```

The fixtures are synthetic, deterministic OHLCV series. They are not intended to represent real assets; they exist to cover different market regimes while keeping the benchmark reproducible.
