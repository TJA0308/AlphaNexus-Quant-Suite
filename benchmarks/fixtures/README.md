# Benchmark Fixtures

These CSV files are deterministic synthetic OHLCV price series. They avoid live market-data timing, provider rate limits, and upstream data revisions so the benchmark measures the AlphaNexus simulation engine instead of `yfinance`.

Regenerate them with:

```bash
python benchmarks/generate_fixtures.py
```
