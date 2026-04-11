import feedparser
import yfinance as yf
from app.services.ticker_map import get_company_names, is_relevant, get_rss_query

def fetch_yfinance_news(ticker: str) -> list:
    stock = yf.Ticker(ticker)
    news = stock.news or []
    headlines = []
    for item in news[:15]:
        title = item.get('content', {}).get('title', '')
        if title and is_relevant(title, ticker):
            headlines.append(title)
    return headlines

def fetch_rss_news(ticker: str) -> list:
    query = get_rss_query(ticker)
    query_encoded = query.replace(" ", "+")
    url = f"https://news.google.com/rss/search?q={query_encoded}&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(url)
    headlines = []
    for entry in feed.entries[:15]:
        title = entry.get("title", "")
        if title and is_relevant(title, ticker):
            headlines.append(title)
    return headlines

def fetch_news(ticker: str) -> tuple[list, bool]:
    headlines = fetch_yfinance_news(ticker)
    rss_used = False
    if len(headlines) < 8:
        rss_headlines = fetch_rss_news(ticker)
        # Avoid duplicates
        existing = set(h.lower() for h in headlines)
        for h in rss_headlines:
            if h.lower() not in existing:
                headlines.append(h)
        rss_used = True
    return headlines, rss_used