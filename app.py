import streamlit as st
from chatbot import RAGChatbot

st.set_page_config(
    page_title="SkyChat AI",
    page_icon="🏨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">

<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0a !important;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(180,148,90,0.13) 0%, transparent 70%),
        radial-gradient(ellipse 60% 40% at 80% 100%, rgba(120,90,50,0.08) 0%, transparent 60%),
        #0a0a0a !important;
    min-height: 100vh;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }

.block-container {
    max-width: 780px !important;
    padding: 0 1.5rem 2rem !important;
    margin: 0 auto !important;
}

* { font-family: 'DM Sans', sans-serif !important; }

.hotel-header {
    text-align: center;
    padding: 3.5rem 1rem 2.5rem;
    border-bottom: 1px solid rgba(180,148,90,0.2);
    margin-bottom: 0;
}

.hotel-crest {
    width: 56px;
    height: 56px;
    margin: 0 auto 1rem;
    border: 1.5px solid rgba(180,148,90,0.5);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    background: rgba(180,148,90,0.06);
}

.hotel-name {
    font-family: 'Playfair Display', serif !important;
    font-size: 2.1rem;
    font-weight: 500;
    color: #e8d5a3;
    letter-spacing: 0.06em;
    line-height: 1.2;
}

.hotel-tagline {
    font-size: 0.75rem;
    color: rgba(180,148,90,0.6);
    letter-spacing: 0.25em;
    text-transform: uppercase;
    margin-top: 0.4rem;
    font-weight: 300;
}

.hotel-divider {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    justify-content: center;
    margin-top: 1.2rem;
}

.hotel-divider-line {
    width: 40px;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(180,148,90,0.4));
}

.hotel-divider-line.right {
    background: linear-gradient(270deg, transparent, rgba(180,148,90,0.4));
}

.hotel-divider-diamond {
    width: 5px;
    height: 5px;
    background: rgba(180,148,90,0.6);
    transform: rotate(45deg);
}

.chat-window {
    padding: 1.5rem 0;
    min-height: 120px;
}

.chat-empty {
    text-align: center;
    padding: 3rem 1rem;
    color: rgba(180,148,90,0.35);
    font-size: 0.88rem;
    letter-spacing: 0.08em;
}

.msg-row {
    display: flex;
    gap: 0.9rem;
    margin-bottom: 1.4rem;
    align-items: flex-start;
}

.msg-row.user { flex-direction: row-reverse; }

.msg-avatar {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    font-weight: 500;
    letter-spacing: 0.02em;
}

.msg-avatar.ai {
    background: rgba(180,148,90,0.12);
    border: 1px solid rgba(180,148,90,0.25);
    color: #b4945a;
    font-family: 'Playfair Display', serif !important;
    font-size: 14px;
}

.msg-avatar.user-av {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    color: rgba(255,255,255,0.5);
    font-size: 16px;
}

.msg-bubble {
    max-width: 78%;
    padding: 0.85rem 1.1rem;
    font-size: 0.93rem;
    line-height: 1.65;
    position: relative;
}

.msg-bubble.ai-bubble {
    background: rgba(20,18,14,0.85);
    border: 1px solid rgba(180,148,90,0.18);
    border-radius: 2px 14px 14px 14px;
    color: rgba(235,220,195,0.9);
}

.msg-bubble.user-bubble {
    background: rgba(180,148,90,0.1);
    border: 1px solid rgba(180,148,90,0.22);
    border-radius: 14px 2px 14px 14px;
    color: rgba(235,220,195,0.85);
}

.msg-meta {
    font-size: 0.7rem;
    color: rgba(180,148,90,0.35);
    margin-top: 0.35rem;
    letter-spacing: 0.04em;
}

.msg-row.user .msg-meta { text-align: right; }

[data-testid="stTextInput"] > div > div {
    background: rgba(15,13,10,0.9) !important;
    border: 1px solid rgba(180,148,90,0.22) !important;
    border-radius: 3px !important;
    transition: border-color 0.25s ease !important;
    box-shadow: none !important;
}

[data-testid="stTextInput"] > div > div:focus-within {
    border-color: rgba(180,148,90,0.5) !important;
    box-shadow: 0 0 0 3px rgba(180,148,90,0.06) !important;
}

[data-testid="stTextInput"] input {
    color: rgba(235,220,195,0.9) !important;
    font-size: 0.93rem !important;
    background: transparent !important;
    padding: 0.75rem 1rem !important;
    caret-color: #b4945a !important;
}

[data-testid="stTextInput"] input::placeholder {
    color: rgba(180,148,90,0.3) !important;
}

[data-testid="stTextInput"] label { display: none !important; }

[data-testid="stButton"] button {
    background: rgba(180,148,90,0.1) !important;
    border: 1px solid rgba(180,148,90,0.35) !important;
    color: #c9a96e !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    font-weight: 500 !important;
    padding: 0.6rem 1.8rem !important;
    border-radius: 2px !important;
    transition: all 0.25s ease !important;
    cursor: pointer !important;
}

[data-testid="stButton"] button:hover {
    background: rgba(180,148,90,0.18) !important;
    border-color: rgba(180,148,90,0.55) !important;
    color: #e8d5a3 !important;
}

.hotel-footer {
    text-align: center;
    padding: 2rem 0 0.5rem;
    font-size: 0.68rem;
    color: rgba(180,148,90,0.2);
    letter-spacing: 0.15em;
    text-transform: uppercase;
}

.status-dot {
    display: inline-block;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #4ade80;
    margin-right: 0.4rem;
    animation: pulse-dot 2.5s ease-in-out infinite;
}

@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.85); }
}

#MainMenu, footer, .stDeployButton { display: none !important; }
</style>
""", unsafe_allow_html=True)


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hotel-header">
    <div class="hotel-crest">🏨</div>
    <div class="hotel-name">SkyChat</div>
    <div class="hotel-tagline"><span class="status-dot"></span>Concierge AI · Available 24 / 7</div>
    <div class="hotel-divider">
        <div class="hotel-divider-line"></div>
        <div class="hotel-divider-diamond"></div>
        <div class="hotel-divider-line right"></div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Session State ─────────────────────────────────────────────────────────────
if "bot" not in st.session_state:
    st.session_state.bot = RAGChatbot()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ── Chat History Display ───────────────────────────────────────────────────────
st.markdown('<div class="chat-window">', unsafe_allow_html=True)

if not st.session_state.chat_history:
    st.markdown("""
    <div class="chat-empty">
        ✦ &nbsp; How may we assist you today? &nbsp; ✦
    </div>
    """, unsafe_allow_html=True)
else:
    for role, msg in st.session_state.chat_history:
        if role == "You":
            st.markdown(f"""
            <div class="msg-row user">
                <div class="msg-avatar user-av">◎</div>
                <div>
                    <div class="msg-bubble user-bubble">{msg}</div>
                    <div class="msg-meta">Guest</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="msg-row">
                <div class="msg-avatar ai">S</div>
                <div>
                    <div class="msg-bubble ai-bubble">{msg}</div>
                    <div class="msg-meta">SkyChat Concierge</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


# ── Input — exact same logic as original, just styled ─────────────────────────
st.markdown("<div style='border-top:1px solid rgba(180,148,90,0.15); padding-top:1.5rem;'></div>",
            unsafe_allow_html=True)

user_input = st.text_input(
    "Ask your question:",
    placeholder="Ask about rooms, dining, amenities...",
    label_visibility="collapsed"
)

if user_input:
    response = st.session_state.bot.chat(user_input)
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("AI", response))
    st.rerun()


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hotel-footer">
    SkyChat Hotel &nbsp;·&nbsp; Powered by AI &nbsp;·&nbsp; All rights reserved
</div>
""", unsafe_allow_html=True)