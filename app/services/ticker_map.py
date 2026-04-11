TICKER_MAP = {
    "RELIANCE.NS": ["Reliance", "RIL", "Reliance Industries"],
    "TCS.NS": ["TCS", "Tata Consultancy", "Tata Consultancy Services"],
    "INFY.NS": ["Infosys", "INFY"],
    "HDFCBANK.NS": ["HDFC Bank", "HDFC"],
    "ICICIBANK.NS": ["ICICI Bank", "ICICI"],
    "SBIN.NS": ["SBI", "State Bank", "State Bank of India"],
    "WIPRO.NS": ["Wipro"],
    "AXISBANK.NS": ["Axis Bank", "Axis"],
    "TATAMOTORS.NS": ["Tata Motors", "Tata Motor"],
    "TATASTEEL.NS": ["Tata Steel"],
    "ADANIENT.NS": ["Adani", "Adani Enterprises"],
    "ADANIPORTS.NS": ["Adani Ports", "APSEZ"],
    "BAJFINANCE.NS": ["Bajaj Finance", "BAF"],
    "BAJAJFINSV.NS": ["Bajaj Finserv"],
    "HINDUNILVR.NS": ["HUL", "Hindustan Unilever"],
    "MARUTI.NS": ["Maruti", "Maruti Suzuki", "MSIL"],
    "SUNPHARMA.NS": ["Sun Pharma", "Sun Pharmaceutical"],
    "ONGC.NS": ["ONGC", "Oil and Natural Gas"],
    "NTPC.NS": ["NTPC"],
    "POWERGRID.NS": ["Power Grid", "PGCIL"],
    "ZOMATO.NS": ["Zomato"],
    "PAYTM.NS": ["Paytm", "One97"],
    "NYKAA.NS": ["Nykaa", "FSN"],
    "DMART.NS": ["DMart", "Avenue Supermarts"],
    "ULTRACEMCO.NS": ["UltraTech", "UltraTech Cement"],
}

def get_company_names(ticker: str):
    return TICKER_MAP.get(ticker.upper(), [ticker.split(".")[0]])

def is_relevant(headline: str, ticker: str) -> bool:
    names = get_company_names(ticker)
    headline_lower = headline.lower()
    return any(name.lower() in headline_lower for name in names)

def get_rss_query(ticker: str) -> str:
    names = get_company_names(ticker)
    company = names[0]
    return f"{company} stock NSE India"