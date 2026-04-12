from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

BULLISH_WORDS = ["rally", "beats", "upgrade", "surges", "record",
                 "profit", "growth", "buyback", "dividend"]

BEARISH_WORDS = ["slump", "miss", "downgrade", "falls", "loss",
                 "weak", "concern", "probe", "debt", "resign",
                 "fraud", "penalty", "fine", "lawsuit", "crash"]

def score_headlines(headlines: list) -> tuple[list, float, str]:
    headlines_list = []
    total_score = 0.0

    for title in headlines:
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