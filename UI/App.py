import os
import sys
import streamlit as st
from workflow import EmotionPredictor
from Report import generate_emotion_report_html
from speech import text_to_speech

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


st.set_page_config(page_title="EMOTION DETECTOR", layout="centered")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif !important;
    }

    /* Title Banner */
    .app-header {
        font-family: 'Space Grotesk', sans-serif !important;
        background-color: #FFDE59;
        border: 4px solid var(--text-color, #000000);
        box-shadow: 6px 6px 0px var(--text-color, #000000);
        padding: 18px;
        text-align: center;
        font-weight: 900;
        font-size: 2.2rem;
        letter-spacing: -1px;
        color: #000000 !important;
        margin-bottom: 25px;
        text-transform: uppercase;
    }

    /* Section Headings */
    .section-title {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1.4rem;
        font-weight: 900;
        text-transform: uppercase;
        margin-top: 25px;
        margin-bottom: 12px;
    }

    /* Input Labels */
    label[data-testid="stWidgetLabel"] p {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 900 !important;
        font-size: 1.1rem !important;
        text-transform: uppercase !important;
    }

    /* Text Area */
    div[data-baseweb="textarea"] {
        border: 4px solid var(--text-color, #000000) !important;
        box-shadow: 6px 6px 0px var(--text-color, #000000) !important;
        border-radius: 0px !important;
    }

    div[data-baseweb="textarea"] textarea {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }

    /* Button */
    div.stButton > button {
        font-family: 'Space Grotesk', sans-serif !important;
        background-color: #FF5757 !important;
        color: #FFFFFF !important;
        font-weight: 900 !important;
        font-size: 1.2rem !important;
        text-transform: uppercase !important;
        border: 4px solid var(--text-color, #000000) !important;
        border-radius: 0px !important;
        box-shadow: 6px 6px 0px var(--text-color, #000000) !important;
        padding: 10px 20px !important;
        transition: all 0.1s ease !important;
    }

    div.stButton > button:hover {
        background-color: #FFDE59 !important;
        color: #000000 !important;
        transform: translate(-2px, -2px) !important;
        box-shadow: 8px 8px 0px var(--text-color, #000000) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown('<div class="app-header">EMOTION DETECTION SYSTEM</div>', unsafe_allow_html=True)

@st.cache_resource
def get_predictor():
    return EmotionPredictor()

try:
    predictor = get_predictor()
except Exception as e:
    st.error(f"SYSTEM ERROR LOADING MODEL: {e}")


text = st.text_area("ENTER TEXT TO ANALYZE:", height=110)
col1, col2 = st.columns([2, 1])
with col2:
    submit = st.button("ANALYZE", use_container_width=True)

if submit:
    if text.strip():
        results = predictor.predict(text)
        report_html, perspective_text = generate_emotion_report_html(results, text)

        st.markdown('<div class="section-title">SENTIMENT ANALYSIS REPORT</div>', unsafe_allow_html=True)
        st.markdown(report_html, unsafe_allow_html=True)
        if perspective_text:
            audio_fp = text_to_speech(f"Your text \n{text} \n{perspective_text}")
            if audio_fp:
                st.caption("LISTEN REPORT:")
                st.audio(audio_fp, format="audio/mp3")
    else:
        st.warning("ERROR: INPUT CANNOT BE EMPTY!")