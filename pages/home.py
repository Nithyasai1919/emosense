import streamlit as st
import numpy as np
import av
import tempfile
import soundfile as sf
import speech_recognition as sr

from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
from transformers import pipeline
from components.translator import translate_to_english
from components.history import add_to_history

# 🌍 Languages
LANGUAGES = {
    "English": "en",
    "Tamil": "ta",
    "Telugu": "te",
    "Hindi": "hi"
}

# 🤖 Load Emotion Model
@st.cache_resource
def load_model():
    return pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base",
        top_k=None
    )

# 🎤 Audio Processor
class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.audio_frames = []

    def recv(self, frame: av.AudioFrame):
        audio = frame.to_ndarray().flatten()
        self.audio_frames.append(audio)
        return frame

# 🎯 MAIN FUNCTION
def show():
    st.markdown("<h1 style='text-align:center; color:white;'>🎤 EmoSense</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#aaa;'>Speak. Sense. Understand.</p>", unsafe_allow_html=True)

    # Language selection
    lang_label = st.selectbox("🌍 Select Language", list(LANGUAGES.keys()))
    lang_code = LANGUAGES[lang_label]

    st.markdown("### 🎤 Speak your voice")

    # 🎤 Start Mic
    ctx = webrtc_streamer(
        key="emotion-audio",
        audio_processor_factory=AudioProcessor,
        media_stream_constraints={"audio": True, "video": False},
    )

    # 🛑 Stop & Analyze
    if ctx.audio_processor:
        if st.button("🛑 Stop & Analyze", use_container_width=True):

            audio_data = ctx.audio_processor.audio_frames

            if len(audio_data) == 0:
                st.warning("⚠️ No audio recorded!")
                return

            # Convert audio
            audio_np = np.concatenate(audio_data)

            # Save temp file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            sf.write(temp_file.name, audio_np, 16000)

            # Speech Recognition
            r = sr.Recognizer()
            with sr.AudioFile(temp_file.name) as source:
                audio = r.record(source)

            try:
                text = r.recognize_google(audio, language=lang_code)
                st.success(f"✅ You said: {text}")

                # Translate → Emotion
                english_text = translate_to_english(text, lang_code)
                model = load_model()
                results = model(english_text)[0]
                results = sorted(results, key=lambda x: x['score'], reverse=True)
                top = results[0]

                # Save history
                add_to_history(text, top['label'], top['score'], lang_label)

                # Store result
                st.session_state.result = {
                    "original": text,
                    "english": english_text,
                    "emotions": results,
                    "language": lang_label
                }

                st.session_state.page = "Result"
                st.rerun()

            except sr.UnknownValueError:
                st.error("❌ Could not understand. Speak clearly!")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
