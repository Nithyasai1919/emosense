import streamlit as st
import speech_recognition as sr
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
            with st.spinner("🔴 Listening... Speak now!"):
                r = sr.Recognizer()
                r.energy_threshold = 300
                r.dynamic_energy_threshold = True
                try:
                    with sr.Microphone() as source:
                        st.markdown("<p style='text-align:center; color:#ff4444;'>🔴 Speak now...</p>", unsafe_allow_html=True)
                        r.adjust_for_ambient_noise(source, duration=0.3)
                        audio = r.listen(source, timeout=10, phrase_time_limit=20)
                    
                    with st.spinner("Analyzing..."):
                        text = r.recognize_google(audio, language=lang_code)
                        st.success(f"✅ You said: {text}")
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
                    st.error("⏱️ No speech detected. Please try again!")
                except sr.UnknownValueError:
                    st.error("❌ Could not understand. Please speak clearly!")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")