import streamlit as st

EMOTION_CONFIG = {
    "joy":      {"emoji": "😊", "color": "#FFD700"},
    "anger":    {"emoji": "😡", "color": "#FF4444"},
    "sadness":  {"emoji": "😢", "color": "#4488FF"},
    "fear":     {"emoji": "😨", "color": "#9B59B6"},
    "disgust":  {"emoji": "🤢", "color": "#27AE60"},
    "surprise": {"emoji": "😲", "color": "#E67E22"},
    "neutral":  {"emoji": "😐", "color": "#95A5A6"},
}

def show():
    st.markdown("<h2 style='text-align:center; color:white;'>📋 History</h2>", unsafe_allow_html=True)
    history = st.session_state.get("history", [])

    if not history:
        st.markdown("<p style='text-align:center; color:#aaa;'>No recordings yet this session.</p>", unsafe_allow_html=True)
        return

    for item in reversed(history):
        cfg = EMOTION_CONFIG.get(item['emotion'], {"emoji": "🤔", "color": "#fff"})
        st.markdown(f"""
        <div style='background:#ffffff11; border-left:4px solid {cfg["color"]}; border-radius:10px; padding:12px; margin:8px 0;'>
            <span style='font-size:24px;'>{cfg["emoji"]}</span>
            <span style='color:white; font-weight:bold; margin-left:8px;'>{item['emotion'].upper()}</span>
            <span style='color:#aaa; font-size:12px; margin-left:8px;'>({round(item['score']*100,1)}%)</span>
            <p style='color:#ccc; margin:5px 0 0 0; font-size:14px;'>"{item['text']}"</p>
            <p style='color:#888; font-size:12px; margin:2px 0 0 0;'>Language: {item['language']}</p>
        </div>
        """, unsafe_allow_html=True)