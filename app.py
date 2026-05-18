import streamlit as st
import plotly.express as px
import pandas as pd
import time
import os
import base64

from utils.preprocessing import preprocess_text
from utils.language import detect_language
from utils.bias import detect_bias
from utils.readability import analyze_readability
from utils.translator import translate_to_english


# ---------------- LOAD CSS ----------------
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
    with open(css_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ---------------- IMAGE TO BASE64 ----------------
def img_to_base64(path):
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode()


# ---------------- FLAG HTML ----------------
def flag_html(flag_url, width=32):
    if flag_url:
        return (
            f'<img src="{flag_url}" width="{width}" '
            f'style="vertical-align:middle; margin-right:10px; border-radius:3px;">'
        )
    return "🌐"


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Text Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()


# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "history" not in st.session_state:
    st.session_state.history = []


# ---------------- LOGO ----------------
logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
logo_base64 = img_to_base64(logo_path)


# ---------------- HEADER ----------------
col1, col2 = st.columns([4, 6])

with col1:
    st.markdown(f"""
<div class="brand-wrap">
    <img src="data:image/png;base64,{logo_base64}" class="logo-img">
    <div>
        <div class="brand-title">Text Analyzer</div>
        <div class="brand-subtitle">Language • Bias • Readability</div>
    </div>
</div>
""", unsafe_allow_html=True)

with col2:
    nav1, nav2, nav3, nav4 = st.columns(4)

    if nav1.button("Home", key="nav_home"):
        st.session_state.page = "Home"

    if nav2.button("Analyze", key="nav_analyze"):
        st.session_state.page = "Analyze"

    if nav3.button("Overview", key="nav_overview"):
        st.session_state.page = "Overview"

    if nav4.button("About", key="nav_about"):
        st.session_state.page = "About"


# ---------------- SIDEBAR HISTORY ----------------
with st.sidebar:
    st.markdown("## 📚 Analysis History")

    if len(st.session_state.history) == 0:
        st.info("No history yet.")
    else:
        for i, item in enumerate(reversed(st.session_state.history), start=1):
            title = f"{i}. {item['language']} | {item['bias']}"

            with st.expander(title):
                preview_text = (
                    item["text"][:250] + "..."
                    if len(item["text"]) > 250
                    else item["text"]
                )

                st.write("**Text:**")
                st.write(preview_text)

                st.markdown(
                    f"**Language:** {flag_html(item.get('flag', ''), 24)} {item['language']}",
                    unsafe_allow_html=True
                )
                st.write(f"**Confidence:** {item['confidence']}%")
                st.write(f"**Bias:** {item['bias']}")
                st.write(f"**Readability:** {item['readability']}%")
                st.write(f"**Level:** {item['level']}")

    st.markdown("---")

    if st.button("Clear History", key="clear_history_btn"):
        st.session_state.history = []
        if "results" in st.session_state:
            del st.session_state["results"]
        st.rerun()


page = st.session_state.page


# ---------------- HOME ----------------
if page == "Home":

    st.markdown("""
<section class="hero">
    <div class="hero-badge">AI Powered Text Intelligence</div>
    <h1>Text Analyzer</h1>
    <p>Analyze language, bias, and readability in a clean professional dashboard.</p>
</section>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="card">
    <h3>What does the Text Analyzer do?</h3>
    <p>
    The Text Analyzer evaluates the difficulty level of text based on readability,
    vocabulary, sentence structure, language detection, and bias tone.
    </p>
</div>
""", unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3)

    with f1:
        st.markdown("""
<div class="feature-box">
    <h4>Language Detection</h4>
    <p>Identifies the input language with confidence score.</p>
</div>
""", unsafe_allow_html=True)

    with f2:
        st.markdown("""
<div class="feature-box">
    <h4>Bias Analysis</h4>
    <p>Detects positive, neutral, or negative tone.</p>
</div>
""", unsafe_allow_html=True)

    with f3:
        st.markdown("""
<div class="feature-box">
    <h4>Readability Score</h4>
    <p>Measures how easy or difficult the text is to read.</p>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="card">
    <h4>How to use</h4>
    <p>Open the Analyze page, enter your text, and click the Analyze button.</p>
</div>
""", unsafe_allow_html=True)


# ---------------- ANALYZE ----------------
elif page == "Analyze":

    st.markdown("""
<section class="page-hero">
    <h2>Analyze Your Text</h2>
    <p>Paste your text below and get instant language, bias, and readability insights.</p>
</section>
""", unsafe_allow_html=True)

    text = st.text_area("Enter Text", height=170)

    btn_left, btn_center, btn_right = st.columns([4, 1.4, 4])

    with btn_center:
        analyze_clicked = st.button("Analyze", key="analyze_btn")

    if analyze_clicked:

        if text.strip() == "":
            st.warning("Please enter text")
            st.stop()

        with st.spinner("Analyzing..."):
            time.sleep(1)

        # -------- NLP LOGIC --------
        lang, flag, lang_conf = detect_language(text)

        translated_text = translate_to_english(text) if lang != "English" else text

        processed = preprocess_text(translated_text)

        bias_label, bias_score, bias_percent = detect_bias(processed)
        readability = analyze_readability(processed)

        if readability["Reading Ease"] >= 80:
            level = "Very Easy"
        elif readability["Reading Ease"] >= 60:
            level = "Easy"
        elif readability["Reading Ease"] >= 40:
            level = "Medium"
        else:
            level = "Difficult"

        current_result = {
            "text": text,
            "language": lang,
            "flag": flag,
            "confidence": round(min(lang_conf, 100), 2),
            "bias": bias_label,
            "readability": readability["Reading Ease"],
            "level": level
        }

        st.session_state["results"] = current_result
        st.session_state.history.append(current_result)

        tab1, tab2, tab3 = st.tabs(["Language", "Bias", "Readability"])

        with tab1:
            st.markdown(f"""
<div class="card result-card">
    <h3>Language Detection</h3>
    <p>
        {flag_html(flag, 32)}
        <b>{lang}</b> ({lang_conf}%)
    </p>
</div>
""", unsafe_allow_html=True)

            if lang != "English":
                st.info(f"Translated Text:\n\n{translated_text}")

        with tab2:
            st.markdown(f"""
<div class="card result-card">
    <h3>Bias Result</h3>
    <p><b>{bias_label}</b></p>
</div>
""", unsafe_allow_html=True)

            st.progress(min(max(int(bias_percent), 0), 100))

            df = pd.DataFrame({
                "Type": list(bias_score.keys()),
                "Score": list(bias_score.values())
            })

            fig = px.bar(df, x="Type", y="Score", text="Score", color="Type")
            st.plotly_chart(fig, width="stretch")

        with tab3:
            st.markdown("""
<div class="card result-card">
    <h3>Readability Analysis</h3>
</div>
""", unsafe_allow_html=True)

            r1, r2, r3 = st.columns(3)

            r1.metric("Reading Ease", readability["Reading Ease"])
            r2.metric("Grade Level", readability["Grade Level"])
            r3.metric("Difficult Words", readability["Difficult Words"])

            if readability["Difficult Words List"]:
                st.write(", ".join(readability["Difficult Words List"]))
            else:
                st.success("No difficult words found")

            st.success(f"Level: {level}")


# ---------------- OVERVIEW ----------------
elif page == "Overview":

    st.markdown("""
<section class="page-hero">
    <h2>Overview</h2>
    <p>Your latest text analysis summary will appear here.</p>
</section>
""", unsafe_allow_html=True)

    if "results" not in st.session_state:
        st.warning("No analysis yet.")
    else:
        data = st.session_state["results"]

        c1, c2, c3, c4 = st.columns(4)

        # Custom language metric card with same height as other metric cards
        c1.markdown(
            f"""
<div class="metric-card-custom">
    <p class="metric-label-custom">Language</p>
    <div class="metric-value-custom">
        {flag_html(data.get('flag', ''), 30)}
        <span>{data['language']}</span>
    </div>
</div>
""",
            unsafe_allow_html=True
        )

        c2.metric("Confidence", f"{data['confidence']}%")
        c3.metric("Bias", data["bias"])
        c4.metric("Readability", f"{data['readability']}%")

        st.markdown("---")

        df = pd.DataFrame({
            "Metric": ["Confidence", "Readability"],
            "Value": [data["confidence"], data["readability"]]
        })

        fig = px.bar(df, x="Metric", y="Value", text="Value", color="Metric")
        st.plotly_chart(fig, width="stretch")

        st.markdown("### Insight")

        if data["readability"] >= 60:
            st.success("Text is easy to read and understand")
        else:
            st.warning("Text may be difficult to read")

        if "Positive" in data["bias"]:
            st.success("Tone is positive")
        elif "Negative" in data["bias"]:
            st.error("Tone is negative")
        else:
            st.info("Tone is neutral")

        st.markdown("## Final Summary")

        st.markdown(f"""
<div class="card">
    <p>
        <b>Language:</b>
        {flag_html(data.get('flag', ''), 28)}
        {data['language']} ({data['confidence']}%)
    </p>
    <p><b>Bias:</b> {data['bias']}</p>
    <p><b>Readability:</b> {data['readability']}%</p>
    <p><b>Level:</b> {data['level']}</p>
</div>
""", unsafe_allow_html=True)


# ---------------- ABOUT ----------------
elif page == "About":

    st.markdown("""
<section class="page-hero">
    <h2>About</h2>
    <p>A simple NLP dashboard for language, bias, and readability analysis.</p>
</section>

<div class="card">
    <h3>About Text Analyzer</h3>
    <p>
    This NLP Analyzer performs language detection, translation, bias analysis,
    and readability scoring using Python-based NLP tools.
    </p>
</div>
""", unsafe_allow_html=True)