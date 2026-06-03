import streamlit as st
from chatbot import RAGChatbot
import time

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SkyChat AI – Hotel Assistant",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f !important;
    color: #e8e0d4 !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(184,142,88,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 50% 40% at 90% 80%, rgba(120,80,40,0.12) 0%, transparent 55%),
        #0a0a0f !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

/* ── Main layout ── */
.main .block-container {
    max-width: 860px !important;
    margin: 0 auto !important;
    padding: 2rem 1.5rem 6rem !important;
}

/* ── Animated grain overlay ── */
body::before {
    content: '';
    position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E");
    opacity: 0.4;
}

/* ── Header ── */
.skychat-header {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    padding: 3rem 0 2.5rem;
    animation: fadeSlideDown 0.9s cubic-bezier(.16,1,.3,1) both;
}

@keyframes fadeSlideDown {
    from { opacity: 0; transform: translateY(-28px); }
    to   { opacity: 1; transform: translateY(0); }
}

.brand-badge {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.32em;
    text-transform: uppercase;
    color: #b88e58;
    background: rgba(184,142,88,0.08);
    border: 1px solid rgba(184,142,88,0.25);
    padding: 0.35rem 1rem;
    border-radius: 100px;
    animation: fadeSlideDown 0.9s 0.15s cubic-bezier(.16,1,.3,1) both;
}

.main-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(2.6rem, 5vw, 3.8rem);
    font-weight: 300;
    letter-spacing: -0.01em;
    line-height: 1.1;
    color: #f0e8dc;
    text-align: center;
    animation: fadeSlideDown 0.9s 0.25s cubic-bezier(.16,1,.3,1) both;
}

.main-title span {
    background: linear-gradient(135deg, #b88e58 0%, #e8c98a 50%, #b88e58 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 4s linear infinite;
}

@keyframes shimmer {
    0%   { background-position: 0% center; }
    100% { background-position: 200% center; }
}

.subtitle {
    font-size: 0.95rem;
    color: rgba(232,224,212,0.45);
    letter-spacing: 0.02em;
    animation: fadeSlideDown 0.9s 0.35s cubic-bezier(.16,1,.3,1) both;
}

/* ── Divider ── */
.gold-divider {
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(184,142,88,0.5), transparent);
    margin: 0.5rem 0 2rem;
    animation: fadeSlideDown 0.9s 0.4s cubic-bezier(.16,1,.3,1) both;
}

/* ── Chat container ── */
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
    padding: 0.5rem 0 1.5rem;
}

/* ── Message bubbles ── */
.msg-row {
    display: flex;
    gap: 0.85rem;
    align-items: flex-start;
    animation: msgIn 0.5s cubic-bezier(.16,1,.3,1) both;
}

@keyframes msgIn {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}

.msg-row.user-row { flex-direction: row-reverse; }

.avatar {
    width: 38px; height: 38px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
    position: relative;
}

.avatar.user-av {
    background: linear-gradient(135deg, #2a1f10, #4a3418);
    border: 1px solid rgba(184,142,88,0.4);
    box-shadow: 0 0 0 3px rgba(184,142,88,0.08);
}

.avatar.ai-av {
    background: linear-gradient(135deg, #0f1a2e, #1a2d4a);
    border: 1px solid rgba(88,140,184,0.4);
    box-shadow: 0 0 0 3px rgba(88,140,184,0.08);
}

.bubble {
    max-width: 72%;
    padding: 0.9rem 1.2rem;
    border-radius: 18px;
    font-size: 0.92rem;
    line-height: 1.65;
    position: relative;
}

.bubble.user-bubble {
    background: linear-gradient(135deg, rgba(184,142,88,0.15), rgba(184,142,88,0.08));
    border: 1px solid rgba(184,142,88,0.22);
    border-bottom-right-radius: 4px;
    color: #f0e8dc;
}

.bubble.ai-bubble {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-bottom-left-radius: 4px;
    color: #d8d0c4;
    backdrop-filter: blur(8px);
}

.bubble-label {
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.35rem;
    opacity: 0.55;
}

.user-bubble .bubble-label { color: #b88e58; }
.ai-bubble   .bubble-label { color: #8ab4d8; }

/* ── Typing indicator ── */
.typing-dots {
    display: flex; gap: 5px; align-items: center;
    padding: 0.3rem 0;
}
.typing-dots span {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #8ab4d8;
    animation: bounce 1.2s infinite;
}
.typing-dots span:nth-child(2) { animation-delay: 0.2s; }
.typing-dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
    0%, 80%, 100% { transform: scale(0.7); opacity: 0.4; }
    40%            { transform: scale(1.1); opacity: 1; }
}

/* ── Empty state ── */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.2rem;
    padding: 3.5rem 1rem;
    text-align: center;
    animation: fadeSlideDown 0.9s 0.5s cubic-bezier(.16,1,.3,1) both;
    opacity: 0;
}

.empty-icon {
    font-size: 3rem;
    filter: drop-shadow(0 0 18px rgba(184,142,88,0.35));
    animation: floatIcon 3.5s ease-in-out infinite;
}

@keyframes floatIcon {
    0%, 100% { transform: translateY(0); }
    50%       { transform: translateY(-8px); }
}

.empty-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.5rem;
    font-weight: 400;
    color: rgba(240,232,220,0.7);
}

.empty-text {
    font-size: 0.88rem;
    color: rgba(232,224,212,0.35);
    max-width: 320px;
    line-height: 1.6;
}

/* ── Quick suggestions ── */
.suggestions {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem;
    justify-content: center;
    margin-top: 0.5rem;
}

.suggestion-chip {
    padding: 0.45rem 1rem;
    border-radius: 100px;
    font-size: 0.8rem;
    background: rgba(184,142,88,0.07);
    border: 1px solid rgba(184,142,88,0.2);
    color: rgba(232,224,212,0.65);
    cursor: pointer;
    transition: all 0.25s ease;
}

.suggestion-chip:hover {
    background: rgba(184,142,88,0.15);
    border-color: rgba(184,142,88,0.45);
    color: #e8c98a;
    transform: translateY(-2px);
}

/* ── Input area ── */
.input-wrapper {
    position: fixed;
    bottom: 0; left: 50%;
    transform: translateX(-50%);
    width: 100%;
    max-width: 860px;
    padding: 1rem 1.5rem 1.5rem;
    background: linear-gradient(to top, #0a0a0f 60%, transparent);
    z-index: 100;
}

.input-inner {
    display: flex;
    gap: 0.75rem;
    align-items: center;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 0.65rem 0.75rem 0.65rem 1.1rem;
    transition: border-color 0.3s, box-shadow 0.3s;
    backdrop-filter: blur(20px);
}

.input-inner:focus-within {
    border-color: rgba(184,142,88,0.45);
    box-shadow: 0 0 0 3px rgba(184,142,88,0.08), 0 8px 32px rgba(0,0,0,0.4);
}

/* Override Streamlit text_input */
[data-testid="stTextInput"] {
    flex: 1;
}

[data-testid="stTextInput"] > div {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}

[data-testid="stTextInput"] input,
[data-testid="stTextInput"] input:focus,
[data-testid="stTextInput"] input:active,
[data-testid="stTextInput"] input:not(:placeholder-shown) {
    background: transparent !important;
    border: none !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    caret-color: #b88e58 !important;
    box-shadow: none !important;
    padding: 0 !important;
    opacity: 1 !important;
}

[data-testid="stTextInput"] input::placeholder {
    color: rgba(232,224,212,0.3) !important;
}

/* Send button */
[data-testid="baseButton-secondary"],
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #b88e58, #e8c98a) !important;
    border: none !important;
    border-radius: 10px !important;
    color: #0a0a0f !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    padding: 0.55rem 1.25rem !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    letter-spacing: 0.03em !important;
    box-shadow: 0 2px 12px rgba(184,142,88,0.35) !important;
    white-space: nowrap !important;
}

[data-testid="stButton"] > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(184,142,88,0.5) !important;
    filter: brightness(1.08) !important;
}

[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
}

/* Clear button */
.clear-btn > button {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: rgba(232,224,212,0.5) !important;
    font-size: 0.82rem !important;
    padding: 0.5rem 0.9rem !important;
    box-shadow: none !important;
}

.clear-btn > button:hover {
    background: rgba(255,80,80,0.1) !important;
    border-color: rgba(255,80,80,0.25) !important;
    color: rgba(255,140,140,0.8) !important;
}

/* ── Stats bar ── */
.stats-bar {
    display: flex;
    gap: 1.5rem;
    justify-content: center;
    padding: 0.6rem 0;
    margin-bottom: 1rem;
    animation: fadeSlideDown 0.9s 0.45s cubic-bezier(.16,1,.3,1) both;
    opacity: 0;
}

.stat-item {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.75rem;
    color: rgba(232,224,212,0.35);
}

.stat-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #4caf50;
    box-shadow: 0 0 6px #4caf50;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.4; }
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: rgba(184,142,88,0.25);
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(184,142,88,0.45); }

/* ── Footer brand ── */
.footer-brand {
    text-align: center;
    font-size: 0.7rem;
    color: rgba(232,224,212,0.18);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 0.5rem;
    font-family: 'DM Sans', sans-serif;
}

.footer-brand strong {
    color: rgba(184,142,88,0.5);
    letter-spacing: 0.1em;
}

/* hide the label above text_input */
[data-testid="stTextInput"] label { display: none !important; }

/* column gaps */
[data-testid="stHorizontalBlock"] {
    gap: 0.6rem !important;
    align-items: center !important;
}

/* ── Responsive ── */
@media (max-width: 600px) {
    .bubble { max-width: 88%; }
    .suggestions { gap: 0.5rem; }
    .suggestion-chip { font-size: 0.75rem; }
}
</style>
""", unsafe_allow_html=True)

# ─── Session State ───────────────────────────────────────────────────────────
if "bot" not in st.session_state:
    st.session_state.bot = RAGChatbot()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "is_typing" not in st.session_state:
    st.session_state.is_typing = False

if "pending_input" not in st.session_state:
    st.session_state.pending_input = None

if "input_key" not in st.session_state:
    st.session_state.input_key = 0

# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="skychat-header">
    <div class="brand-badge">✦ &nbsp; S.S_AI &nbsp; ✦</div>
    <div class="main-title">SkyChat <span>AI</span></div>
    <div class="subtitle">Your personal luxury hotel concierge, always available</div>
</div>
<div class="gold-divider"></div>
""", unsafe_allow_html=True)

# ─── Status bar ──────────────────────────────────────────────────────────────
msg_count = len([r for r, _ in st.session_state.chat_history if r == "You"])
st.markdown(f"""
<div class="stats-bar">
    <div class="stat-item"><div class="stat-dot"></div> AI Online</div>
    <div class="stat-item">· &nbsp; {msg_count} message{"s" if msg_count != 1 else ""} today</div>
    <div class="stat-item">· &nbsp; 🏨 SkyHotel Concierge</div>
</div>
""", unsafe_allow_html=True)

# ─── Chat History ─────────────────────────────────────────────────────────────
if not st.session_state.chat_history:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">🏨</div>
        <div class="empty-title">Welcome to SkyChat</div>
        <div class="empty-text">
            I'm your dedicated hotel AI assistant. Ask me anything about
            rooms, amenities, dining, check-in, or local recommendations.
        </div>
        <div class="suggestions">
            <div class="suggestion-chip">🛏️ Room availability</div>
            <div class="suggestion-chip">🍽️ Restaurant hours</div>
            <div class="suggestion-chip">🏊 Pool & spa info</div>
            <div class="suggestion-chip">📍 Local attractions</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for i, (role, msg) in enumerate(st.session_state.chat_history):
        if role == "You":
            st.markdown(f"""
            <div class="msg-row user-row" style="animation-delay:{i*0.05}s">
                <div class="avatar user-av">🧑</div>
                <div class="bubble user-bubble">
                    <div class="bubble-label">You</div>
                    {msg}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="msg-row" style="animation-delay:{i*0.05}s">
                <div class="avatar ai-av">🤖</div>
                <div class="bubble ai-bubble">
                    <div class="bubble-label">SkyChat AI</div>
                    {msg}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Typing indicator
    if st.session_state.is_typing:
        st.markdown("""
        <div class="msg-row">
            <div class="avatar ai-av">🤖</div>
            <div class="bubble ai-bubble">
                <div class="typing-dots">
                    <span></span><span></span><span></span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ─── Input Area ──────────────────────────────────────────────────────────────
st.markdown('<div class="input-wrapper"><div class="input-inner">', unsafe_allow_html=True)

col1, col2, col3 = st.columns([8, 1.4, 1.1])

with col1:
    user_input = st.text_input(
        label="message",
        placeholder="Ask about rooms, dining, amenities…",
        key=f"user_msg_{st.session_state.input_key}",
        label_visibility="hidden",
    )

with col2:
    send_clicked = st.button("✦ Send", use_container_width=True)

with col3:
    st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
    clear_clicked = st.button("Clear", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # input-inner

# Footer brand inside wrapper
st.markdown("""
<div class="footer-brand">Powered by <strong>S.S_AI</strong> · SkyChat Hotel Intelligence</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # input-wrapper

# ─── Logic ───────────────────────────────────────────────────────────────────
if clear_clicked:
    st.session_state.chat_history = []
    st.session_state.input_key += 1
    st.rerun()

trigger = (send_clicked and user_input.strip()) or \
          (user_input.strip() and user_input != st.session_state.get("_last_input", ""))

if trigger:
    msg = user_input.strip()
    st.session_state["_last_input"] = ""
    st.session_state.is_typing = True
    st.session_state.pending_input = msg
    st.session_state.input_key += 1
    st.rerun()

# Phase 2: typing dots are showing, now fetch response
if st.session_state.is_typing and st.session_state.pending_input:
    msg = st.session_state.pending_input
    response = st.session_state.bot.chat(msg)
    st.session_state.chat_history.append(("You", msg))
    st.session_state.chat_history.append(("AI", response))
    st.session_state.is_typing = False
    st.session_state.pending_input = None
    st.rerun()
