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
    st.markdown("<h2 style='text-align:center; color:white;'>🎯 Result</h2>", unsafe_allow_html=True)

    if not st.session_state.result:
        st.markdown("<p style='text-align:center; color:#aaa;'>No result yet. Go to Home and record!</p>", unsafe_allow_html=True)
        return

    data = st.session_state.result
    emotions = data["emotions"]
    top = emotions[0]
    cfg = EMOTION_CONFIG.get(top['label'], {"emoji": "🤔", "color": "#fff"})

    st.markdown(f"""
    <div style='background:{cfg["color"]}22; border:2px solid {cfg["color"]}; border-radius:20px; padding:20px; text-align:center; margin-bottom:20px;'>
        <div style='font-size:64px;'>{cfg["emoji"]}</div>
        <div style='color:white; font-size:28px; font-weight:bold;'>{top['label'].upper()}</div>
        <div style='color:#ddd; font-size:16px;'>Confidence: {round(top['score']*100, 1)}%</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"<p style='color:#ccc;'>🗣️ You said: <i>{data['original']}</i></p>", unsafe_allow_html=True)
    st.markdown("<p style='color:white; font-weight:bold; margin-top:20px;'>All Emotions:</p>", unsafe_allow_html=True)

    for e in emotions:
        ecfg = EMOTION_CONFIG.get(e['label'], {"emoji": "🤔", "color": "#fff"})
        pct = round(e['score'] * 100, 1)
        st.markdown(f"""
        <div style='margin:8px 0;'>
            <div style='display:flex; justify-content:space-between; color:white; margin-bottom:3px;'>
                <span>{ecfg["emoji"]} {e['label'].capitalize()}</span>
                <span>{pct}%</span>
            </div>
            <div style='background:#333; border-radius:10px; height:18px; width:100%;'>
                <div style='background:{ecfg["color"]}; width:{pct}%; height:18px; border-radius:10px;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)