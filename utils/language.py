import fasttext
import os
import urllib.request

MODEL_PATH = "lid.176.bin"

if not os.path.exists(MODEL_PATH):
    urllib.request.urlretrieve(
        "https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin",
        MODEL_PATH
    )

model = fasttext.load_model(MODEL_PATH)

LANG_MAP = {
    "en": ("English", "🇺🇸"),
    "hi": ("Hindi", "🇮🇳"),
    "it": ("Italian", "🇮🇹"),
    "fr": ("French", "🇫🇷"),
    "de": ("German", "🇩🇪"),
    "es": ("Spanish", "🇪🇸"),
    "ko": ("Korean", "🇰🇷"),
    "kn": ("Kannada", "🇮🇳")
}

def detect_language(text):
    try:
        prediction = model.predict(text)

        lang_code = prediction[0][0].replace("__label__", "")
        confidence = prediction[1][0]

        lang_name, flag = LANG_MAP.get(lang_code, (lang_code.upper(), "🌐"))

        return lang_name, flag, round(confidence * 100, 2)

    except Exception as e:
        print("ERROR:", e)
        return "Unknown", 0.0