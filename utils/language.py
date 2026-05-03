from langdetect import detect_langs, DetectorFactory

DetectorFactory.seed = 0

LANG_MAP = {
    "en": ("English", "🇺🇸"),
    "hi": ("Hindi", "🇮🇳"),
    "es": ("Spanish", "🇪🇸"),
    "fr": ("French", "🇫🇷"),
    "de": ("German", "🇩🇪"),
    "it": ("Italian", "🇮🇹"),
    "pt": ("Portuguese", "🇵🇹"),
    "ru": ("Russian", "🇷🇺"),
    "ja": ("Japanese", "🇯🇵"),
    "ko": ("Korean", "🇰🇷"),
    "zh-cn": ("Chinese", "🇨🇳"),
    "zh-tw": ("Chinese", "🇨🇳"),
    "ar": ("Arabic", "🇸🇦"),
    "bn": ("Bengali", "🇧🇩"),
    "ta": ("Tamil", "🇮🇳"),
    "te": ("Telugu", "🇮🇳"),
    "mr": ("Marathi", "🇮🇳"),
    "gu": ("Gujarati", "🇮🇳"),
    "pa": ("Punjabi", "🇮🇳"),
    "ur": ("Urdu", "🇵🇰"),
    "kn": ("Kannada", "🇮🇳"),
    "nl": ("Dutch", "🇳🇱"),
    "tr": ("Turkish", "🇹🇷"),
    "pl": ("Polish", "🇵🇱"),
    "ro": ("Romanian", "🇷🇴"),
    "sv": ("Swedish", "🇸🇪"),
    "no": ("Norwegian", "🇳🇴"),
    "da": ("Danish", "🇩🇰"),
    "fi": ("Finnish", "🇫🇮"),
}

def detect_language(text):
    try:
        clean_text = text.strip()

        if not clean_text:
            return "Unknown", "🌐", 0.0

        # Very short text is unreliable
        if len(clean_text.split()) < 3:
            return "Text too short", "🌐", 0.0

        result = detect_langs(clean_text)[0]

        lang_code = result.lang
        confidence = round(result.prob * 100, 2)

        lang_name, flag = LANG_MAP.get(lang_code, (lang_code.upper(), "🌐"))

        return lang_name, flag, confidence

    except Exception as e:
        print("LANGUAGE DETECTION ERROR:", e)
        return "Unknown", "🌐", 0.0