from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

BULLISH_WORDS = ["rally", "beats", "upgrade", "surges", "record",
                 "profit", "growth", "buyback", "dividend"]

BEARISH_WORDS = ["slump", "miss", "downgrade", "falls", "loss",
                 "weak", "concern", "probe", "debt", "resign",
                 "fraud", "penalty", "fine", "lawsuit", "crash"]

NEGATION_PHRASES = [
    "aren't as", "not as", "isn't", "aren't", "no longer",
    "despite", "although", "however", "but ", "issues allocating",
    "may have issues", "as good as they seem", "not good"
]

JUNK_SOURCES = [
    "tradingview", "upstox.com/stocks", "yahoo finance singapore",
    "equitypandit", "business today stock", "live stock price",
    "share price today", "stock price today", "nse/bse"
]

def is_junk_headline(headline: str) -> bool:
    h = headline.lower()
    
    junk_patterns = [
        "share price today", "stock price today",
        "live stock price", "stock analysis -",
        "stock price and chart", "quote and history",
        "share price -", "largest shareholder sees value"
    ]
    return any(p in h for p in junk_patterns)

def apply_negation_dampening(score: float, headline: str) -> tuple[float, bool]:
    h = headline.lower()
    if any(phrase in h for phrase in NEGATION_PHRASES):
        return round(score * 0.6, 2), True  # score, negation_triggered
    return score, False

def score_headlines(headlines: list) -> tuple[list, float, str]:
    headlines_list = []
    total_score = 0.0

    for title in headlines:
        # Drop junk headlines
        if is_junk_headline(title):
            continue

        vader_dict = analyzer.polarity_scores(title)
        base_score = vader_dict['compound']

        title_lower = title.lower()
        booster = 0.0
        for word in BULLISH_WORDS:
            if word in title_lower:
                booster += 0.10
        for word in BEARISH_WORDS:
            if word in title_lower:
                booster -= 0.10

        final_score = max(-1.0, min(1.0, base_score + booster))
        final_score, negation_triggered = apply_negation_dampening(final_score, title)

        #force neutral if negation triggered and score is still bullish
        if negation_triggered and final_score>0.15:
            final_score=0.0

        if final_score >= 0.05:
            label = "Bullish"
        elif final_score <= -0.05:
            label = "Bearish"
        else:
            label = "Neutral"

        total_score += final_score
        headlines_list.append({
            "headline": title,
            "score": round(final_score, 2),
            "label": label
        })

    count = len(headlines_list)
    avg_score = round(total_score / count, 2) if count > 0 else 0.0

    if avg_score >= 0.05:
        overall_label = "Bullish"
    elif avg_score <= -0.05:
        overall_label = "Bearish"
    else:
        overall_label = "Neutral"

    return headlines_list, avg_score, overall_label