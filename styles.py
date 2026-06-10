import streamlit as st

def apply_custom_theme():
    """Injects high-end institutional dark mode styling to completely override Streamlit defaults."""
    st.markdown("""
        <style>
        /* 1. Complete Background and Text Polish */
        .stApp {
            background-color: #0d1117 !important;
            color: #c9d1d9 !important;
        }
        
        /* 2. Transform Default Metric Cards into Premium Neon Modules */
        div[data-testid="stMetric"] {
            background: linear-gradient(135deg, #161b22 0%, #0d1117 100%) !important;
            border: 1px solid #30363d !important;
            border-radius: 12px !important;
            padding: 20px 25px !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
            transition: all 0.3s ease-in-out !important;
        }
        div[data-testid="stMetric"]:hover {
            border-color: #58a6ff !important;
            box-shadow: 0 0 15px rgba(88, 166, 255, 0.15) !important;
            transform: translateY(-2px);
        }
        
        /* 3. Text Color Specifications inside Metrics */
        div[data-testid="stMetricValue"] {
            color: #58a6ff !important;
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif !important;
            font-size: 34px !important;
            font-weight: 700 !important;
        }
        div[data-testid="stMetricLabel"] {
            color: #8b949e !important;
            font-size: 13px !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 1.5px !important;
        }
        
        /* 4. Overhaul Sidebar Panel Controls */
        section[data-testid="stSidebar"] {
            background-color: #161b22 !important;
            border-right: 1px solid #30363d !important;
        }
        
        /* 5. Custom Interactive Execution Button Glow */
        .stButton>button {
            width: 100% !important;
            background: linear-gradient(90deg, #1f6feb 0%, #238636 100%) !important;
            color: #ffffff !important;
            font-weight: 700 !important;
            letter-spacing: 1px !important;
            text-transform: uppercase !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 12px 0px !important;
            box-shadow: 0 4px 12px rgba(31, 111, 235, 0.3) !important;
            transition: all 0.2s ease !important;
        }
        .stButton>button:hover {
            transform: scale(1.02) !important;
            box-shadow: 0 6px 20px rgba(31, 111, 235, 0.5) !important;
        }
        
        /* 6. Clean Navigation Tabs styling */
        button[data-baseweb="tab"] {
            color: #8b949e !important;
            font-weight: 600 !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #58a6ff !important;
            border-bottom-color: #58a6ff !important;
        }
        </style>
    """, unsafe_allow_html=True)
