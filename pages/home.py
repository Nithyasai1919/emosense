import streamlit as st
import speech_recognition as sr
import os
from components.translator import translate_to_english
from components.history import add_to_history
from transformers import pipeline

LANGUAGES = {
    "English": "en",
    "Tamil": "ta",
    "Telugu": "te",
    "Hindi": "hi"
}

@st.cache_resource
def load_model():
    return pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=None)

def show():
    st.markdown("<h1 style='text-align:center; color:white; font-size:36px;'>🎤 EmoSense</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#aaa;'>Speak. Sense. Understand.</p>", unsafe_allow_html=True)

    lang_label = st.selectbox("🌍 Select Language", list(LANGUAGES.keys()))
    lang_code = LANGUAGES[lang_label]

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<p style='text-align:center; color:#aaa; font-size:14px;'>Click the button, speak, then wait 2 seconds for auto-detection</p>", unsafe_allow_html=True)

    col = st.columns([1,2,1])[1]
    with col:
       if st.button("🎤 Record & Analyze", use_container_width=True):

    # Detect if running on Streamlit Cloud
    is_cloud = os.getenv("STREAMLIT_SERVER_HEADLESS") == "true"

    if is_cloud:
        st.warning("🎤 Microphone not supported here. Please upload audio.")

        audio_file = st.file_uploader("Upload your voice", type=["wav"])

        if audio_file is not None:
            r = sr.Recognizer()
            with sr.AudioFile(audio_file) as source:
                audio = r.record(source)

            text = r.recognize_google(audio, language=lang_code)
            st.success(f"✅ You said: {text}")

    else:
        # LOCAL MIC (your original code)
        with st.spinner("🔴 Listening... Speak now!"):
            r = sr.Recognizer()
            r.energy_threshold = 300
            r.dynamic_energy_threshold = True

            try:
                with sr.Microphone() as source:
                    st.markdown("<p style='text-align:center; color:#ff4444;'>🔴 Speak now...</p>", unsafe_allow_html=True)
                    r.adjust_for_ambient_noise(source, duration=0.3)
                    audio = r.listen(source, timeout=10, phrase_time_limit=20)

                text = r.recognize_google(audio, language=lang_code)
                st.success(f"✅ You said: {text}")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
