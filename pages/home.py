import streamlit as st
import speech_recognition as sr
import os
from components.translator import translate_to_english
from components.history import add_to_history
from transformers import pipeline

# Language options
LANGUAGES = {
    "English": "en",
    "Tamil": "ta",
    "Telugu": "te",
    "Hindi": "hi"
}

# Load emotion model
@st.cache_resource
def load_model():
    return pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base",
        top_k=None
    )

def show():
    st.markdown("<h1 style='text-align:center; color:white;'>🎤 EmoSense</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#aaa;'>Speak. Sense. Understand.</p>", unsafe_allow_html=True)

    lang_label = st.selectbox("🌍 Select Language", list(LANGUAGES.keys()))
    lang_code = LANGUAGES[lang_label]

    st.markdown("<br>", unsafe_allow_html=True)

    # 🎤 BUTTON
    if st.button("🎤 Record & Analyze", use_container_width=True):

        is_cloud = os.getenv("STREAMLIT_SERVER_HEADLESS") == "true"

        # 🌐 STREAMLIT CLOUD (UPLOAD)
        if is_cloud:
            st.warning("🎤 Microphone not supported here. Please upload audio.")

            audio_file = st.file_uploader("Upload your voice (.wav)", type=["wav"])

            if audio_file is not None:
                r = sr.Recognizer()
                with sr.AudioFile(audio_file) as source:
                    audio = r.record(source)

                try:
                    text = r.recognize_google(audio, language=lang_code)
                    st.success(f"✅ You said: {text}")

                    # Process emotion
                    english_text = translate_to_english(text, lang_code)
                    model = load_model()
                    results = model(english_text)[0]
                    results = sorted(results, key=lambda x: x['score'], reverse=True)
                    top = results[0]

                    add_to_history(text, top['label'], top['score'], lang_label)

                    st.session_state.result = {
                        "original": text,
                        "english": english_text,
                        "emotions": results,
                        "language": lang_label
                    }

                    st.session_state.page = "Result"
                    st.rerun()

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

        # 💻 LOCAL MIC (VS CODE)
        else:
            with st.spinner("🔴 Listening... Speak now!"):
                r = sr.Recognizer()
                r.energy_threshold = 300
                r.dynamic_energy_threshold = True

                try:
                    with sr.Microphone() as source:
                        st.markdown("🔴 Speak now...")
                        r.adjust_for_ambient_noise(source, duration=0.3)
                        audio = r.listen(source, timeout=10, phrase_time_limit=20)

                    text = r.recognize_google(audio, language=lang_code)
                    st.success(f"✅ You said: {text}")

                    # Process emotion
                    english_text = translate_to_english(text, lang_code)
                    model = load_model()
                    results = model(english_text)[0]
                    results = sorted(results, key=lambda x: x['score'], reverse=True)
                    top = results[0]

                    add_to_history(text, top['label'], top['score'], lang_label)

                    st.session_state.result = {
                        "original": text,
                        "english": english_text,
                        "emotions": results,
                        "language": lang_label
                    }

                    st.session_state.page = "Result"
                    st.rerun()

                except sr.WaitTimeoutError:
                    st.error("⏱️ No speech detected. Try again!")
                except sr.UnknownValueError:
                    st.error("❌ Could not understand. Speak clearly!")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
