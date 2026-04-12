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
    "LT.NS": ["Larsen & Toubro", "L&T", "Larsen and Toubro"],
    "HCLTECH.NS": ["HCL Technologies", "HCL Tech", "HCL"],
    "TECHM.NS": ["Tech Mahindra", "TechM"],
    "BAJFINANCE.NS": ["Bajaj Finance", "BAF"],
    "KOTAKBANK.NS": ["Kotak Mahindra", "Kotak Bank", "Kotak"],
}

import yfinance as yf

def get_company_names(ticker: str) -> list:
    # Check hardcoded map first
    names = TICKER_MAP.get(ticker.upper())
    if names:
        return names

    # Unknown ticker — fetch from yfinance
    try:
        info = yf.Ticker(ticker).info
        long_name = info.get("longName", "")
        short_name = info.get("shortName", "")
        names = []
        if long_name:
            names.append(long_name)
            # Add first word as shorthand e.g. "Tata" from "Tata Communications"
            first_word = long_name.split()[0]
            if len(first_word) > 4:
                names.append(first_word)
        if short_name and short_name not in names:
            names.append(short_name)
        # Always add raw ticker as fallback
        names.append(ticker.split(".")[0])
        return names if names else [ticker.split(".")[0]]
    except:
        return [ticker.split(".")[0]]

def is_relevant(headline: str, ticker: str) -> bool:
    names = get_company_names(ticker)
    headline_lower = headline.lower()
    return any(name.lower() in headline_lower for name in names)

def get_rss_query(ticker: str) -> str:
    names = get_company_names(ticker)
    company = names[0]
    return f"{company} stock NSE India"