import streamlit as st

def show():
    st.markdown("<h2 style='text-align:center; color:white;'>⚙️ Settings</h2>", unsafe_allow_html=True)

    st.markdown("""
    <div style='background:#ffffff11; border-radius:15px; padding:20px; margin:10px 0;'>
        <p style='color:white; font-size:18px; font-weight:bold;'>📱 EmoSense</p>
        <p style='color:#aaa;'>Version 1.0.0</p>
        <p style='color:#aaa;'>Speak. Sense. Understand.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background:#ffffff11; border-radius:15px; padding:20px; margin:10px 0;'>
        <p style='color:white; font-size:16px; font-weight:bold;'>👥 Team</p>
        <p style='color:#aaa;'>Built with ❤️ for project submission</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background:#ffffff11; border-radius:15px; padding:20px; margin:10px 0;'>
        <p style='color:white; font-size:16px; font-weight:bold;'>🤖 Model</p>
        <p style='color:#aaa;'>j-hartmann/emotion-english-distilroberta-base</p>
        <p style='color:#aaa;'>Detects: Joy, Anger, Sadness, Fear, Disgust, Surprise, Neutral</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🗑️ Clear Session History", use_container_width=True):
        st.session_state.history = []
        st.success("History cleared!")