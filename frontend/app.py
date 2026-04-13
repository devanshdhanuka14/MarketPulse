import streamlit as st
import requests
from config import API_BASE_URL

st.set_page_config(
    page_title="MarketPulse",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
<style>
    .history-card {
        background: #1e1e1e;
        border-radius: 8px;
        padding: 10px 16px;
        margin-bottom: 6px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .badge {
        padding: 3px 12px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
        color: white;
    }
    .bullish { background: #00c853; }
    .bearish { background: #ff1744; }
    .neutral { background: #555555; }
    div[data-testid="stTabs"] button {
        font-size: 1rem;
        font-weight: 600;
        padding: 8px 24px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("# 📈 MarketPulse")
st.caption("Financial news sentiment for Indian stocks — VADER + Finance keyword scoring")
st.divider()

def normalize_ticker(ticker: str) -> str:
    ticker = ticker.strip().upper()
    if ticker and "." not in ticker:
        ticker = ticker + ".NS"
    return ticker

def extract_source(headline: str) -> tuple[str, str]:
    if " - " in headline:
        parts = headline.rsplit(" - ", 1)
        return parts[0].strip(), parts[1].strip()
    return headline.strip(), ""

def sort_headlines(headlines: list, overall_label: str) -> list:
    order = {"Bullish": 0, "Bearish": 1, "Neutral": 2}
    if overall_label == "Bearish":
        order = {"Bearish": 0, "Bullish": 1, "Neutral": 2}
    elif overall_label == "Neutral":
        order = {"Neutral": 0, "Bullish": 1, "Bearish": 2}
    return sorted(headlines, key=lambda h: order.get(h["label"], 3))

def render_headline_card(h: dict):
    label = h["label"]
    score = h["score"]
    bg = "#1a3a1a" if label == "Bullish" else "#3a1a1a" if label == "Bearish" else "#2a2a2a"
    badge_color = "#00c853" if label == "Bullish" else "#ff1744" if label == "Bearish" else "#888888"
    title, source = extract_source(h["headline"])
    source_html = f'<span style="color:#888;font-size:0.75rem;">📰 {source}</span>' if source else ""
    st.markdown(f"""
    <div style="background:{bg};border-radius:8px;padding:12px 16px;margin-bottom:8px;">
        <div style="margin-bottom:4px;">{source_html}</div>
        <div style="font-size:0.95rem;color:#f0f0f0;margin-bottom:8px;">{title}</div>
        <span style="background:{badge_color};color:white;padding:2px 10px;border-radius:12px;font-size:0.8rem;font-weight:600;">{label}</span>
        <span style="color:#aaa;font-size:0.8rem;margin-left:10px;">Score: {score}</span>
    </div>
    """, unsafe_allow_html=True)

def render_history_card(item: dict):
    label = item["result_label"]
    badge_class = label.lower()
    time = item["queried_at"][:16].replace("T", " ")
    st.markdown(f"""
    <div class="history-card">
        <div style="display:flex;align-items:center;gap:12px;">
            <span style="font-size:1rem;font-weight:700;color:#f0f0f0;">{item['ticker']}</span>
            <span class="badge {badge_class}">{label}</span>
        </div>
        <span style="color:#888;font-size:0.8rem;">🕐 {time} UTC</span>
    </div>
    """, unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📊  Sentiment", "⚖️  Compare Stocks", "🕐  Recent Searches"])

with tab1:
    st.subheader("Stock Sentiment Analysis")
    col_input, col_btn = st.columns([4, 1])
    with col_input:
        ticker = normalize_ticker(st.text_input(
            "",
            placeholder="Enter NSE ticker — e.g. RELIANCE, TCS, INFY",
            label_visibility="collapsed"
        ))
    with col_btn:
        analyse = st.button("Analyse →", use_container_width=True)

    if analyse:
        if not ticker:
            st.warning("Please enter a ticker")
        else:
            with st.spinner(f"Fetching sentiment for {ticker}..."):
                try:
                    res = requests.get(f"{API_BASE_URL}/sentiment/{ticker}", timeout=30)
                    if res.status_code == 200:
                        st.session_state["result"] = res.json()
                    else:
                        st.error(f"API error: {res.status_code}")
                except Exception as e:
                    st.error(f"Could not connect to backend: {e}")

    if "result" in st.session_state:
        data = st.session_state["result"]
        label = data["label"]

        st.divider()

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            color = "green" if label == "Bullish" else "red" if label == "Bearish" else "gray"
            st.markdown(f"## :{color}[{label}]")
            st.caption("Overall Verdict")
        with m2:
            st.metric("Sentiment Score", data["score"])
        with m3:
            st.metric("Headlines Analysed", data["headline_count"])
        with m4:
            st.metric("Data Source", "Cache ⚡" if data["cached"] else "Live 🔴")

        if data["low_confidence"]:
            st.warning(f"⚠️ Low confidence — {data['low_confidence_reason']}")

        st.divider()

        bullish_h = [h for h in data["headlines"] if h["label"] == "Bullish"]
        bearish_h = [h for h in data["headlines"] if h["label"] == "Bearish"]
        neutral_h = [h for h in data["headlines"] if h["label"] == "Neutral"]

        c1, c2, c3 = st.columns(3)
        c1.metric("🟢 Bullish", len(bullish_h))
        c2.metric("🔴 Bearish", len(bearish_h))
        c3.metric("⚪ Neutral", len(neutral_h))

        st.markdown("")
        sorted_headlines = sort_headlines(data["headlines"], label)
        for h in sorted_headlines:
            render_headline_card(h)

with tab2:
    st.subheader("Compare Up To 3 Stocks")
    col1, col2, col3 = st.columns(3)
    with col1:
        t1 = normalize_ticker(st.text_input("Ticker 1", placeholder="RELIANCE"))
    with col2:
        t2 = normalize_ticker(st.text_input("Ticker 2", placeholder="TCS"))
    with col3:
        t3 = normalize_ticker(st.text_input("Ticker 3", placeholder="INFY"))

    if st.button("Compare →", use_container_width=True):
        tickers = [t for t in [t1, t2, t3] if t]
        if len(tickers) < 2:
            st.warning("Enter at least 2 tickers")
        else:
            results = []
            with st.spinner("Fetching sentiment for all tickers..."):
                for t in tickers:
                    try:
                        res = requests.get(f"{API_BASE_URL}/sentiment/{t}", timeout=30)
                        if res.status_code == 200:
                            results.append(res.json())
                    except:
                        st.error(f"Failed to fetch {t}")
            if results:
                st.session_state["compare_results"] = results

    if "compare_results" in st.session_state:
        results = st.session_state["compare_results"]
        st.divider()
        cols = st.columns(len(results))

        for i, data in enumerate(results):
            with cols[i]:
                label = data["label"]
                color = "green" if label == "Bullish" else "red" if label == "Bearish" else "gray"
                st.markdown(f"#### {data['ticker']}")
                st.markdown(f"### :{color}[{label}]")
                st.metric("Score", data["score"])
                st.metric("Headlines", data["headline_count"])

                bullish = sum(1 for h in data["headlines"] if h["label"] == "Bullish")
                bearish = sum(1 for h in data["headlines"] if h["label"] == "Bearish")
                neutral = sum(1 for h in data["headlines"] if h["label"] == "Neutral")
                st.caption(f"🟢 {bullish} · 🔴 {bearish} · ⚪ {neutral}")

                if data["low_confidence"]:
                    st.warning("⚠️ Low confidence")

                if data["headlines"]:
                    st.divider()
                    st.caption("Top headline")
                    top = sort_headlines(data["headlines"], label)[0]
                    title, source = extract_source(top["headline"])
                    st.markdown(f"*{title}*")
                    if source:
                        st.caption(f"📰 {source}")

        labels = [r["label"] for r in results]
        bullish_count = labels.count("Bullish")
        bearish_count = labels.count("Bearish")
        st.divider()
        if bullish_count > bearish_count:
            st.success("📈 Overall market mood across selected stocks — Bullish")
        elif bearish_count > bullish_count:
            st.error("📉 Overall market mood across selected stocks — Bearish")
        else:
            st.info("➡️ Overall market mood across selected stocks — Mixed")

with tab3:
    st.subheader("Recent Searches")
    st.caption("Last 20 tickers queried via MarketPulse API")

    col_btn, col_empty = st.columns([1, 3])
    with col_btn:
        load = st.button("Load History", use_container_width=True)

    if load:
        try:
            res = requests.get(f"{API_BASE_URL}/history", timeout=10)
            if res.status_code == 200:
                st.session_state["history"] = res.json()
            else:
                st.error("Could not load history")
        except Exception as e:
            st.error(f"Connection error: {e}")

    if "history" in st.session_state:
        history = st.session_state["history"]
        if not history:
            st.info("No searches yet")
        else:
            bullish_total = sum(1 for h in history if h["result_label"] == "Bullish")
            bearish_total = sum(1 for h in history if h["result_label"] == "Bearish")
            neutral_total = sum(1 for h in history if h["result_label"] == "Neutral")

            s1, s2, s3 = st.columns(3)
            s1.metric("🟢 Bullish Queries", bullish_total)
            s2.metric("🔴 Bearish Queries", bearish_total)
            s3.metric("⚪ Neutral Queries", neutral_total)

            st.markdown("")
            for item in history:
                render_history_card(item)

st.divider()
st.markdown(
    "Made by [Devansh Dhanuka](https://www.linkedin.com/in/devanshdhanuka/) · "
    "Built with FastAPI · VADER · PostgreSQL · Streamlit",
    unsafe_allow_html=True
)