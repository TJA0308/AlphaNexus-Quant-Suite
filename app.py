from __future__ import annotations

from datetime import date, datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from alphanexus.backtest import BacktestConfig, run_backtest
from alphanexus.data import fetch_prices
from alphanexus.strategies import StrategyConfig
from styles import apply_custom_theme


ASSET_POOL = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Nvidia": "NVDA",
    "Amazon": "AMZN",
    "Alphabet": "GOOGL",
    "Bitcoin": "BTC-USD",
}

STRATEGY_LABELS = {
    "SMA Crossover": "sma_crossover",
    "RSI Mean Reversion": "rsi_mean_reversion",
    "Bollinger Breakout": "bollinger_breakout",
}

DEFAULT_START_DATE = date.today() - timedelta(days=365)
DEFAULT_END_DATE = date.today()

DEFAULT_WIDGETS = {
    "asset_choice": "Apple",
    "strategy_choice": "SMA Crossover",
    "interval_choice": "1d",
    "start_date": DEFAULT_START_DATE,
    "end_date": DEFAULT_END_DATE,
    "starting_cash": 10_000,
    "fee_bps": 5,
    "slippage_bps": 5,
    "allocation_pct": 100,
    "fast_window": 20,
    "slow_window": 50,
    "rsi_window": 14,
    "oversold": 30,
    "overbought": 70,
    "band_window": 20,
    "band_std": 2.0,
}


st.set_page_config(page_title="Strategy Backtest Workbench", layout="wide")
apply_custom_theme()

if "last_run" not in st.session_state:
    st.session_state.last_run = None
if "run_history" not in st.session_state:
    st.session_state.run_history = []
for key, value in DEFAULT_WIDGETS.items():
    if key not in st.session_state:
        st.session_state[key] = value


@st.cache_data(ttl=900)
def load_prices(ticker: str, start: date, end: date, interval: str) -> pd.DataFrame:
    return fetch_prices(ticker, start, end, interval)


def format_percent(value: float) -> str:
    return f"{value * 100:,.2f}%"


def format_strategy_summary(strategy_name: str, config: StrategyConfig) -> str:
    if strategy_name == "sma_crossover":
        return f"Go long when the {config.fast_window}-day average is above the {config.slow_window}-day average."
    if strategy_name == "rsi_mean_reversion":
        return f"Go long when RSI falls below {config.oversold:g}; exit when RSI rises above {config.overbought:g}."
    return f"Go long after a close above the upper band; exit below the center line."


def metrics_to_csv(metrics: dict[str, float | int]) -> bytes:
    summary = pd.DataFrame([metrics])
    return summary.to_csv(index=False).encode("utf-8")


def build_history_row(
    ticker: str,
    strategy_label: str,
    start_date: date,
    end_date: date,
    metrics: dict[str, float | int],
) -> dict[str, str | float | int]:
    return {
        "Run time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Ticker": ticker,
        "Strategy": strategy_label,
        "Period": f"{start_date} to {end_date}",
        "Return": float(metrics["total_return"]),
        "Benchmark": float(metrics["benchmark_return"]),
        "Max drawdown": float(metrics["max_drawdown"]),
        "Sharpe": float(metrics["sharpe_ratio"]),
        "Trades": int(metrics["trade_count"]),
    }


def build_equity_chart(result: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=result["date"],
            y=result["portfolio_value"],
            mode="lines",
            name="Strategy",
            line={"color": "#2f80ed", "width": 3},
        )
    )
    fig.add_trace(
        go.Scatter(
            x=result["date"],
            y=result["benchmark_value"],
            mode="lines",
            name="Buy and hold",
            line={"color": "#9aa4b2", "width": 2, "dash": "dot"},
        )
    )
    fig.update_layout(
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font={"color": "#17202a"},
        height=430,
        margin={"l": 10, "r": 10, "t": 20, "b": 10},
        legend={"orientation": "h", "y": 1.05},
        yaxis_title="Portfolio value",
        xaxis={"gridcolor": "#e4e8ef", "zerolinecolor": "#e4e8ef"},
        yaxis={"gridcolor": "#e4e8ef", "zerolinecolor": "#e4e8ef"},
    )
    return fig


def build_drawdown_chart(result: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=result["date"],
            y=result["drawdown"] * 100,
            mode="lines",
            name="Drawdown",
            fill="tozeroy",
            line={"color": "#d64545", "width": 2},
        )
    )
    fig.update_layout(
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font={"color": "#17202a"},
        height=260,
        margin={"l": 10, "r": 10, "t": 20, "b": 10},
        yaxis_title="Drawdown %",
        showlegend=False,
        xaxis={"gridcolor": "#e4e8ef", "zerolinecolor": "#e4e8ef"},
        yaxis={"gridcolor": "#e4e8ef", "zerolinecolor": "#e4e8ef"},
    )
    return fig


def build_price_chart(result: pd.DataFrame) -> go.Figure:
    buys = result[result["trade_signal"] > 0]
    sells = result[result["trade_signal"] < 0]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=result["date"],
            y=result["close"],
            mode="lines",
            name="Close",
            line={"color": "#d4d9e2", "width": 2},
        )
    )
    fig.add_trace(
        go.Scatter(
            x=buys["date"],
            y=buys["close"],
            mode="markers",
            name="Buy",
            marker={"color": "#22c55e", "size": 10, "symbol": "triangle-up"},
        )
    )
    fig.add_trace(
        go.Scatter(
            x=sells["date"],
            y=sells["close"],
            mode="markers",
            name="Sell",
            marker={"color": "#ef4444", "size": 10, "symbol": "triangle-down"},
        )
    )
    fig.update_layout(
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font={"color": "#17202a"},
        height=360,
        margin={"l": 10, "r": 10, "t": 20, "b": 10},
        legend={"orientation": "h", "y": 1.05},
        yaxis_title="Close price",
        xaxis={"gridcolor": "#e4e8ef", "zerolinecolor": "#e4e8ef"},
        yaxis={"gridcolor": "#e4e8ef", "zerolinecolor": "#e4e8ef"},
    )
    return fig


st.markdown(
    """
    <section class="hero-panel">
        <div>
            <p class="eyebrow">Market research tool</p>
            <h1>Strategy Backtest Workbench</h1>
            <p class="hero-copy">Test simple long-only trading rules, compare them against buy-and-hold, and inspect the assumptions behind the result.</p>
        </div>
        <div class="hero-facts">
            <span>Fees</span>
            <span>Slippage</span>
            <span>Benchmark</span>
            <span>Trade ledger</span>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Backtest controls")
    st.caption("Start with the preset, then change one input at a time.")
    if st.button("Load demo preset", use_container_width=True):
        for key, value in DEFAULT_WIDGETS.items():
            st.session_state[key] = value
        st.session_state.last_run = None
        st.rerun()

    st.markdown("### Market")
    selected_asset = st.selectbox("Asset", list(ASSET_POOL.keys()), key="asset_choice")
    ticker = ASSET_POOL[selected_asset]
    interval = st.selectbox("Interval", ["1d", "1h"], key="interval_choice")
    start_date = st.date_input("Start date", key="start_date")
    end_date = st.date_input("End date", key="end_date")

    st.markdown("### Strategy")
    strategy_label = st.selectbox("Strategy", list(STRATEGY_LABELS.keys()), key="strategy_choice")
    strategy_name = STRATEGY_LABELS[strategy_label]

    if strategy_name == "sma_crossover":
        fast_window = st.slider("Fast SMA window", 5, 50, key="fast_window")
        slow_window = st.slider("Slow SMA window", 20, 200, key="slow_window")
        strategy_config = StrategyConfig(
            name="sma_crossover",
            fast_window=fast_window,
            slow_window=slow_window,
        )
    elif strategy_name == "rsi_mean_reversion":
        rsi_window = st.slider("RSI window", 5, 40, key="rsi_window")
        oversold = st.slider("Oversold threshold", 10, 45, key="oversold")
        overbought = st.slider("Overbought threshold", 55, 90, key="overbought")
        strategy_config = StrategyConfig(
            name="rsi_mean_reversion",
            rsi_window=rsi_window,
            oversold=oversold,
            overbought=overbought,
        )
    else:
        band_window = st.slider("Band window", 10, 80, key="band_window")
        band_std = st.slider("Band width", 0.5, 3.0, key="band_std")
        strategy_config = StrategyConfig(
            name="bollinger_breakout",
            band_window=band_window,
            band_std=band_std,
        )

    st.markdown("### Portfolio")
    starting_cash = st.number_input("Starting cash", min_value=1000, step=1000, key="starting_cash")
    allocation = st.slider("Capital allocation", 10, 100, key="allocation_pct") / 100

    st.markdown("### Costs")
    fee_bps = st.slider("Fee, basis points", 0, 50, key="fee_bps")
    slippage_bps = st.slider("Slippage, basis points", 0, 50, key="slippage_bps")

    run_clicked = st.button("Run backtest", type="primary", use_container_width=True)

current_assumptions = {
    "Ticker": ticker,
    "Strategy": strategy_label,
    "Date range": f"{start_date} to {end_date}",
    "Interval": interval,
    "Starting cash": f"${starting_cash:,.0f}",
    "Fee": f"{fee_bps} bps per trade",
    "Slippage": f"{slippage_bps} bps per trade",
    "Allocation": f"{allocation * 100:.0f}% of available cash",
}

if start_date >= end_date:
    st.error("Start date must be before end date.")
elif run_clicked:
    try:
        prices = load_prices(ticker, start_date, end_date, interval)
        result, metrics = run_backtest(
            prices,
            strategy_config,
            BacktestConfig(
                starting_cash=float(starting_cash),
                fee_bps=float(fee_bps),
                slippage_bps=float(slippage_bps),
                allocation=float(allocation),
                interval=interval,
            ),
        )
        st.session_state.last_run = {
            "ticker": ticker,
            "strategy_label": strategy_label,
            "strategy_name": strategy_name,
            "strategy_config": strategy_config,
            "result": result,
            "metrics": metrics,
            "assumptions": current_assumptions,
        }
        st.session_state.run_history = [
            build_history_row(ticker, strategy_label, start_date, end_date, metrics),
            *st.session_state.run_history,
        ][:8]
    except Exception as exc:
        st.error(f"Could not run backtest: {exc}")
        st.stop()

last_run = st.session_state.last_run

if last_run is None:
    st.markdown(
        """
        <div class="empty-state">
            <div>
                <p class="eyebrow">Ready to run</p>
                <h2>Start with the AAPL demo preset.</h2>
                <p>The default setup runs a one-year SMA crossover backtest with fees, slippage, benchmark comparison, and downloadable results.</p>
            </div>
            <div class="mini-flow">
                <span>1. Choose inputs</span>
                <span>2. Run backtest</span>
                <span>3. Review risk</span>
                <span>4. Export evidence</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Current setup")
    setup_cols = st.columns(4)
    for index, (label, value) in enumerate(current_assumptions.items()):
        setup_cols[index % 4].markdown(f"**{label}**  \n{value}")

    st.markdown("### Assumptions")
    c1, c2, c3 = st.columns(3)
    c1.markdown("**Long-only**  \nThe simulator holds cash or one long position.")
    c2.markdown("**Close-price signals**  \nSignals use the downloaded close price.")
    c3.markdown("**Costs included**  \nFees and slippage are deducted on executed trades.")
else:
    result = last_run["result"]
    metrics = last_run["metrics"]
    assumptions = last_run["assumptions"]
    strategy_config = last_run["strategy_config"]
    strategy_name = last_run["strategy_name"]
    strategy_label = last_run["strategy_label"]
    ticker = last_run["ticker"]

    metric_cols = st.columns(6)
    metric_cols[0].metric("Ending equity", f"${metrics['ending_equity']:,.2f}")
    metric_cols[1].metric("Strategy return", format_percent(metrics["total_return"]))
    metric_cols[2].metric("Benchmark", format_percent(metrics["benchmark_return"]))
    metric_cols[3].metric("Max drawdown", format_percent(metrics["max_drawdown"]))
    metric_cols[4].metric("Sharpe", f"{metrics['sharpe_ratio']:.2f}")
    metric_cols[5].metric("Win rate", format_percent(metrics["win_rate"]))

    alpha = metrics["total_return"] - metrics["benchmark_return"]
    verdict = "outperformed" if alpha > 0 else "underperformed"
    st.markdown(
        f"""
        <div class="result-summary">
            <strong>{ticker} / {strategy_label}</strong>
            <span>The strategy {verdict} buy-and-hold by {format_percent(abs(alpha))} over this period.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="assumption-bar">
            <span>{ticker}</span>
            <span>{strategy_label}</span>
            <span>{assumptions["Interval"]} bars</span>
            <span>{assumptions["Fee"]}</span>
            <span>{assumptions["Slippage"]}</span>
            <span>{metrics['trade_count']} completed trades</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab_performance, tab_trades, tab_assumptions, tab_export = st.tabs(["Performance", "Trades", "Assumptions", "Exports"])
    with tab_performance:
        st.plotly_chart(build_equity_chart(result), use_container_width=True)
        left, right = st.columns([2, 1])
        with left:
            st.plotly_chart(build_price_chart(result), use_container_width=True)
        with right:
            st.plotly_chart(build_drawdown_chart(result), use_container_width=True)

        if st.session_state.run_history:
            st.subheader("Recent runs")
            history = pd.DataFrame(st.session_state.run_history)
            display_history = history.copy()
            for column in ["Return", "Benchmark", "Max drawdown"]:
                display_history[column] = display_history[column].map(format_percent)
            display_history["Sharpe"] = display_history["Sharpe"].map(lambda value: f"{value:.2f}")
            st.dataframe(display_history, use_container_width=True, hide_index=True)

    with tab_trades:
        trades = result[result["trade_signal"] != 0][
            ["date", "close", "trade_signal", "shares", "cash", "portfolio_value", "realized_pnl"]
        ].copy()
        trades["side"] = trades["trade_signal"].map({1: "Buy", -1: "Sell"})
        display_trades = trades[["date", "side", "close", "shares", "cash", "portfolio_value", "realized_pnl"]]
        if display_trades.empty:
            st.info("This configuration did not execute any trades in the selected period.")
        else:
            st.dataframe(display_trades, use_container_width=True, hide_index=True)

    with tab_assumptions:
        left, right = st.columns([1, 1])
        with left:
            st.subheader("Strategy rule")
            st.write(format_strategy_summary(strategy_name, strategy_config))
            st.subheader("Execution model")
            st.write("Long-only portfolio. The simulator moves between cash and one position, applying fee and slippage assumptions on executed trades.")
            st.caption("This is a research tool, not a prediction model or trading recommendation.")
        with right:
            st.subheader("Model assumptions")
            for label, value in assumptions.items():
                st.markdown(f"**{label}:** {value}")
            st.caption("The benchmark is buy-and-hold over the same selected period.")
        st.subheader("Recent data")
        st.dataframe(result.tail(100), use_container_width=True, hide_index=True)

    with tab_export:
        st.write("Download the results for review, documentation, or further analysis.")
        export_cols = st.columns(3)
        export_cols[0].download_button(
            "Download trade ledger",
            data=display_trades.to_csv(index=False).encode("utf-8"),
            file_name=f"{ticker.lower()}_{strategy_name}_trades.csv",
            mime="text/csv",
            use_container_width=True,
        )
        export_cols[1].download_button(
            "Download equity curve",
            data=result.to_csv(index=False).encode("utf-8"),
            file_name=f"{ticker.lower()}_{strategy_name}_equity.csv",
            mime="text/csv",
            use_container_width=True,
        )
        export_cols[2].download_button(
            "Download summary",
            data=metrics_to_csv(metrics),
            file_name=f"{ticker.lower()}_{strategy_name}_summary.csv",
            mime="text/csv",
            use_container_width=True,
        )
        if st.session_state.run_history:
            st.download_button(
                "Download run history",
                data=pd.DataFrame(st.session_state.run_history).to_csv(index=False).encode("utf-8"),
                file_name="backtest_run_history.csv",
                mime="text/csv",
                use_container_width=True,
            )
