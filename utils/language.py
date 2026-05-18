import os
import re
import fasttext

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "lid.176.bin")


LANG_MAP = {
    "en": ("English", "https://flagcdn.com/w40/gb.png"),
    "hi": ("Hindi", "https://flagcdn.com/w40/in.png"),
    "fr": ("French", "https://flagcdn.com/w40/fr.png"),
    "es": ("Spanish", "https://flagcdn.com/w40/es.png"),
    "de": ("German", "https://flagcdn.com/w40/de.png"),
    "it": ("Italian", "https://flagcdn.com/w40/it.png"),
    "pt": ("Portuguese", "https://flagcdn.com/w40/pt.png"),
    "ru": ("Russian", "https://flagcdn.com/w40/ru.png"),
    "ja": ("Japanese", "https://flagcdn.com/w40/jp.png"),
    "ko": ("Korean", "https://flagcdn.com/w40/kr.png"),
    "zh": ("Chinese", "https://flagcdn.com/w40/cn.png"),
    "ar": ("Arabic", "https://flagcdn.com/w40/sa.png"),
    "bn": ("Bengali", "https://flagcdn.com/w40/bd.png"),
    "ta": ("Tamil", "https://flagcdn.com/w40/in.png"),
    "te": ("Telugu", "https://flagcdn.com/w40/in.png"),
    "mr": ("Marathi", "https://flagcdn.com/w40/in.png"),
    "gu": ("Gujarati", "https://flagcdn.com/w40/in.png"),
    "pa": ("Punjabi", "https://flagcdn.com/w40/in.png"),
    "ur": ("Urdu", "https://flagcdn.com/w40/pk.png"),
    "kn": ("Kannada", "https://flagcdn.com/w40/in.png"),
    "ml": ("Malayalam", "https://flagcdn.com/w40/in.png"),
    "or": ("Odia", "https://flagcdn.com/w40/in.png"),
    "ne": ("Nepali", "https://flagcdn.com/w40/np.png"),
    "nl": ("Dutch", "https://flagcdn.com/w40/nl.png"),
    "tr": ("Turkish", "https://flagcdn.com/w40/tr.png"),
    "pl": ("Polish", "https://flagcdn.com/w40/pl.png"),
    "ro": ("Romanian", "https://flagcdn.com/w40/ro.png"),
    "sv": ("Swedish", "https://flagcdn.com/w40/se.png"),
    "no": ("Norwegian", "https://flagcdn.com/w40/no.png"),
    "da": ("Danish", "https://flagcdn.com/w40/dk.png"),
    "fi": ("Finnish", "https://flagcdn.com/w40/fi.png"),
}


try:
    model = fasttext.load_model(MODEL_PATH)
except Exception as e:
    model = None
    print("FASTTEXT MODEL LOAD ERROR:", e)


def detect_language(text):
    try:
        clean_text = text.strip()
        clean_text = re.sub(r"\s+", " ", clean_text)

        if not clean_text:
            return "Unknown", "", 0.0

        if len(clean_text) < 3:
            return "Text too short", "", 0.0

        if model is None:
            return "Model not loaded", "", 0.0

        labels, scores = model.predict(clean_text, k=1)

        lang_code = labels[0].replace("__label__", "")
        confidence = round(float(scores[0]) * 100, 2)

        lang_name, flag_url = LANG_MAP.get(lang_code, (lang_code.upper(), ""))

        return lang_name, flag_url, confidence

    except Exception as e:
        print("FASTTEXT LANGUAGE DETECTION ERROR:", e)
        return "Unknown", "", 0.0