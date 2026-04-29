import textstat

def analyze_readability(text):

    # Hindi detection
    if any('\u0900' <= char <= '\u097F' for char in text):
        return {
            "Reading Ease": 0,
            "Grade Level": 0,
            "Difficult Words": 0,
            "Difficult Words List": [],
            "Note": "Readability not supported for Hindi"
        }

    score = textstat.flesch_reading_ease(text)

    # Clamp between 0–100
    score = max(0, min(100, round(score, 2)))

    return {
        "Reading Ease": score,
        "Grade Level": round(textstat.flesch_kincaid_grade(text), 2),
        "Difficult Words": textstat.difficult_words(text),
        "Difficult Words List": textstat.difficult_words_list(text)
    }