from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

# Hindi sentiment words
HINDI_POSITIVE = ["अच्छा", "पसंद", "खुश", "बढ़िया", "शानदार"]
HINDI_NEGATIVE = ["बुरा", "नफरत", "घटिया", "बेकार", "खराब"]

def detect_bias(text):
    text_lower = text.lower()

    # Hindi detection
    if any('\u0900' <= char <= '\u097F' for char in text):

        pos = sum(word in text for word in HINDI_POSITIVE)
        neg = sum(word in text for word in HINDI_NEGATIVE)

        if pos > neg:
            label = "Positive :) (80%)"
            return label, {"pos": 1, "neu": 0, "neg": 0, "compound": 0.8}, 80

        elif neg > pos:
            label = "Toxic / Negative :( (80%)"
            return label, {"pos": 0, "neu": 0, "neg": 1, "compound": -0.8}, 20

        else:
            return "Neutral :| (50%)", {"pos": 0, "neu": 1, "neg": 0, "compound": 0}, 50

    # English (VADER)
    score = analyzer.polarity_scores(text)
    compound = score["compound"]

    bias_percent = round((compound + 1) * 50, 2)

    if compound >= 0.05:
        label = f"Non-Toxic / Positive ({bias_percent}%)"
    elif compound <= -0.05:
        label = f"Toxic / Negative ({bias_percent}%)"
    else:
        label = f"Neutral ({bias_percent}%)"

    return label, score, bias_percent