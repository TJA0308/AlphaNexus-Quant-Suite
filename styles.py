import streamlit as st


def apply_custom_theme() -> None:
    st.markdown(
        """
        <style>
        :root {
            --page: #f6f8fb;
            --panel: #ffffff;
            --panel-muted: #eef3f8;
            --text: #17202a;
            --muted: #5c6673;
            --border: #d9e0ea;
            --accent: #2563eb;
            --green: #0f8b6f;
            --red: #c2410c;
        }

        .stApp {
            background: var(--page);
            color: var(--text);
        }

        .block-container {
            max-width: 1380px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        h1, h2, h3 {
            color: var(--text);
            letter-spacing: 0;
        }

        p, li, label, span {
            color: var(--text);
        }

        [data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid var(--border);
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: var(--text);
        }

        [data-testid="stSidebar"] .stCaptionContainer p {
            color: var(--muted);
        }

        .hero-panel {
            align-items: center;
            background: linear-gradient(135deg, #ffffff 0%, #eef5ff 62%, #edf8f4 100%);
            border: 1px solid var(--border);
            border-radius: 12px;
            display: flex;
            justify-content: space-between;
            gap: 2rem;
            margin-bottom: 1.2rem;
            padding: 1.4rem 1.5rem;
        }

        .hero-panel h1 {
            font-size: 2rem;
            line-height: 1.15;
            margin: 0.1rem 0 0.45rem;
        }

        .hero-copy {
            color: var(--muted);
            font-size: 0.98rem;
            margin: 0;
            max-width: 720px;
        }

        .eyebrow {
            color: var(--accent);
            font-size: 0.76rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            margin: 0;
            text-transform: uppercase;
        }

        .hero-facts,
        .assumption-bar,
        .mini-flow {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }

        .hero-facts {
            justify-content: flex-end;
            min-width: 260px;
        }

        .hero-facts span,
        .assumption-bar span,
        .mini-flow span {
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 999px;
            color: #334155;
            font-size: 0.8rem;
            font-weight: 650;
            padding: 0.42rem 0.7rem;
            white-space: nowrap;
        }

        [data-testid="stMetric"] {
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 10px;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
            padding: 1rem;
        }

        [data-testid="stMetricLabel"] {
            color: var(--muted);
            font-size: 0.76rem;
            font-weight: 700;
            text-transform: uppercase;
        }

        [data-testid="stMetricValue"] {
            color: var(--text);
            font-size: 1.45rem;
            font-weight: 750;
        }

        .result-summary,
        .assumption-bar,
        .empty-state {
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 12px;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
        }

        .result-summary {
            align-items: center;
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            margin: 1rem 0 0.75rem;
            padding: 0.85rem 1rem;
        }

        .result-summary strong {
            color: var(--text);
        }

        .result-summary span {
            color: var(--muted);
        }

        .assumption-bar {
            align-items: center;
            margin: 0.8rem 0 1rem;
            padding: 0.75rem;
        }

        .assumption-bar span {
            background: var(--panel-muted);
        }

        .empty-state {
            align-items: center;
            display: flex;
            justify-content: space-between;
            gap: 2rem;
            margin-bottom: 1rem;
            padding: 1.3rem 1.4rem;
        }

        .empty-state h2 {
            font-size: 1.45rem;
            margin: 0.2rem 0 0.45rem;
        }

        .empty-state p {
            color: var(--muted);
            margin: 0;
            max-width: 680px;
        }

        div[data-testid="stTabs"] button {
            color: var(--muted);
            font-weight: 700;
        }

        div[data-testid="stTabs"] button[aria-selected="true"] {
            color: var(--accent);
        }

        .stButton > button,
        .stDownloadButton > button {
            border-radius: 9px;
            font-weight: 750;
        }

        .stButton > button[kind="primary"] {
            background: var(--accent);
            border: 1px solid var(--accent);
        }

        [data-testid="stAlert"] {
            border-radius: 10px;
        }

        @media (max-width: 900px) {
            .hero-panel,
            .empty-state,
            .result-summary {
                align-items: flex-start;
                flex-direction: column;
            }

            .hero-facts {
                justify-content: flex-start;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
