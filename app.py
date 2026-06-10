import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# IMPORT YOUR CUSTOM MODULES (Architectural Separation)
from strategies import run_bollinger_breakout, run_rsi_momentum
from styles import apply_custom_theme

st.set_page_config(page_title="AlphaNexus Suite Pro", layout="wide")
apply_custom_theme() # Instantly applies your CSS styling

st.title("🏛️ AlphaNexus: Advanced Quantitative Sandbox")
st.caption("A multi-strategy, modular backtesting software framework.")

asset_pool = {
    "Nvidia (NVDA)": "NVDA", "Apple (AAPL)": "AAPL", "Microsoft (MSFT)": "MSFT",
    "Amazon (AMZN)": "AMZN", "Google (GOOGL)": "GOOGL", "Bitcoin (BTC-USD)": "BTC-USD"
}

# 1. SIDEBAR CONFIGURATION LAYER
st.sidebar.header("📁 Suite Controller")
selected_label = st.sidebar.selectbox("Target Core Security", list(asset_pool.keys()))
target_ticker = asset_pool[selected_label]

# NEW FEATURE: Interactive Strategy Selection Menu
st.sidebar.markdown("---")
st.sidebar.subheader("Algorithmic Model Selection")
strategy_choice = st.sidebar.selectbox("Active Core Logic", ["Bollinger Band Breakout", "RSI Momentum"])

# Dynamic Sidebar Sliders based on which strategy is active
if strategy_choice == "Bollinger Band Breakout":
    ma_window = st.sidebar.slider("Channel Baseline (Days)", 10, 50, 20)
    dev_multiplier = st.sidebar.slider("Band Sensitivity (Std Dev)", 0.5, 2.5, 1.5, 0.1)
else:
    rsi_window = st.sidebar.slider("RSI Lookback Period", 5, 30, 14)
    oversold_line = st.sidebar.slider("Oversold Threshold (Buy)", 15, 40, 30)
    overbought_line = st.sidebar.slider("Overbought Threshold (Sell)", 60, 85, 70)

st.sidebar.markdown("---")
execute_analytics = st.sidebar.button("⚙️ Execute Strategy Core", use_container_width=True)

# 2. CACHED PIPELINE INGESTION
@st.cache_data
def ingest_market_records(ticker):
    df = yf.download(ticker, period="60d", interval="1h", multi_level_index=False)
    df = df[['Close']].reset_index()
    df.columns = ['Date', 'Close']
    return df

base_data = ingest_market_records(target_ticker)

# 3. STRATEGY COMPUTATION ROUTER
if execute_analytics:
    working_df = base_data.copy()
    
    # Routing logic based on user selection
    if strategy_choice == "Bollinger Band Breakout":
        df = run_bollinger_breakout(working_df, ma_window, dev_multiplier)
    else:
        df = run_rsi_momentum(working_df, rsi_window, oversold_line, overbought_line)
        
    # State tracking & engine simulation processing
    starting_capital = 10000.0
    df['Daily_Return_Asset'] = df['Close'].pct_change()
    
    current_position, positions = 0, []
    for idx, row in df.iterrows():
        if row['Buy_Signal'] == 1: current_position = 1
        elif row['Sell_Signal'] == 1: current_position = 0
        positions.append(current_position)
        
    df['Position'] = positions
    df['Position'] = df['Position'].shift(1).fillna(0)
    df['Strategy_Daily_Return'] = df['Daily_Return_Asset'] * df['Position']
    df['Portfolio_Value'] = starting_capital * (1 + df['Strategy_Daily_Return']).cumprod()
    
    # Financial Analytics Layer
    final_equity = df['Portfolio_Value'].iloc[-1]
    strategy_return = ((final_equity - starting_capital) / starting_capital) * 100
    market_return = ((df['Close'].iloc[-1] - df['Close'].iloc[0]) / df['Close'].iloc[0]) * 100
    
    df['Peak'] = df['Portfolio_Value'].cummax()
    df['Drawdown'] = (df['Portfolio_Value'] - df['Peak']) / df['Peak']
    max_drawdown = df['Drawdown'].min() * 100
    sharpe = (df['Strategy_Daily_Return'].mean() / df['Strategy_Daily_Return'].std()) * np.sqrt(252) if df['Strategy_Daily_Return'].std() != 0 else 0
    
    # UI Render Components
    st.success(f"Successfully processed {strategy_choice} model for {selected_label}.")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Final Balance", f"${final_equity:,.2f}")
    m2.metric("Net Return", f"{strategy_return:.2f}%", f"{strategy_return - market_return:.2f}% vs Market")
    m3.metric("Max Risk Drop", f"{max_drawdown:.2f}%")
    m4.metric("Sharpe Efficiency", f"{sharpe:.2f}")
    
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["📊 Performance Charting", "📋 Signal Ledger Analytics"])
    with tab1:
        if strategy_choice == "Bollinger Band Breakout":
            st.line_chart(df.set_index('Date')[['Close', 'Upper_Band', 'Lower_Band', 'Portfolio_Value']])
        else:
            # For RSI view, chart the asset closing value alongside the running indicator channel
            st.line_chart(df.set_index('Date')[['Close', 'Portfolio_Value']])
            st.subheader("Oscillator Tracking")
            st.line_chart(df.set_index('Date')[['RSI', 'Upper_Band', 'Lower_Band']])
    with tab2:
        st.dataframe(df[df['Buy_Signal'] == 1].head(10), use_container_width=True)
else:
    st.info("👈 Open the sidebar control workspace panel, select your model variant, and trigger the calculation core engine.")
