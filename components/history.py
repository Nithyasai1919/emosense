import streamlit as st

def add_to_history(text, emotion, score, language):
    if "history" not in st.session_state:
        st.session_state.history = []
    st.session_state.history.append({
        "text": text,
        "emotion": emotion,
        "score": score,
        "language": language
    })

def get_history():
    if "history" not in st.session_state:
        st.session_state.history = []
    return st.session_state.history