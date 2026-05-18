from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

HINDI_POSITIVE = ["अच्छा", "पसंद", "खुश", "बढ़िया", "शानदार"]
HINDI_NEGATIVE = ["बुरा", "नफरत", "घटिया", "बेकार", "खराब"]


def detect_bias(text):
    text_lower = text.lower()

    # Hindi detection
    if any('\u0900' <= char <= '\u097F' for char in text):

        pos = sum(word in text for word in HINDI_POSITIVE)
        neg = sum(word in text for word in HINDI_NEGATIVE)

        if pos > neg:
            label = "Positive"
            return label, {"Positive": 80, "Neutral": 20, "Negative": 0}, 80

        elif neg > pos:
            label = "Negative"
            return label, {"Positive": 0, "Neutral": 20, "Negative": 80}, 80

        else:
            label = "Neutral"
            return label, {"Positive": 0, "Neutral": 100, "Negative": 0}, 100

    # English / translated text sentiment
    score = analyzer.polarity_scores(text)
    compound = score["compound"]

    positive_score = round(score["pos"] * 100, 2)
    neutral_score = round(score["neu"] * 100, 2)
    negative_score = round(score["neg"] * 100, 2)

    if compound >= 0.05:
        label = "Positive"
        final_percent = positive_score

    elif compound <= -0.05:
        label = "Negative"
        final_percent = negative_score

    else:
        label = "Neutral"
        final_percent = neutral_score

    bias_score = {
        "Positive": positive_score,
        "Neutral": neutral_score,
        "Negative": negative_score
    }

    return f"{label} ({final_percent}%)", bias_score, final_percent