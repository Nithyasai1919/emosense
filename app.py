import streamlit as st

st.set_page_config(page_title="EmoSense", page_icon="🎤", layout="centered")

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stApp { background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460); }
.block-container { padding-top: 20px; max-width: 480px; margin: auto; }
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "Home"
if "history" not in st.session_state:
    st.session_state.history = []
if "result" not in st.session_state:
    st.session_state.result = None

page = st.session_state.page

if page == "Home":
    from pages.home import show
    show()
elif page == "Result":
    from pages.result import show
    show()
elif page == "History":
    from pages.history_page import show
    show()
elif page == "Settings":
    from pages.settings import show
    show()

st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("🏠\nHome", use_container_width=True):
        st.session_state.page = "Home"
        st.rerun()
with col2:
    if st.button("🎯\nResult", use_container_width=True):
        st.session_state.page = "Result"
        st.rerun()
with col3:
    if st.button("📋\nHistory", use_container_width=True):
        st.session_state.page = "History"
        st.rerun()
with col4:
    if st.button("⚙️\nSettings", use_container_width=True):
        st.session_state.page = "Settings"
        st.rerun()