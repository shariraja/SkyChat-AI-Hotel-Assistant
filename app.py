import streamlit as st
from chatbot import RAGChatbot

st.set_page_config(page_title="SkyChat AI", page_icon="🏨")

st.title("🏨 SkyChat AI - Hotel Assistant")

# Load chatbot once
if "bot" not in st.session_state:
    st.session_state.bot = RAGChatbot()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input box
user_input = st.text_input("Ask your question:")

if user_input:
    response = st.session_state.bot.chat(user_input)

    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("AI", response))

# Display chat history
for role, msg in st.session_state.chat_history:
    if role == "You":
        st.markdown(f"**🧑 You:** {msg}")
    else:
        st.markdown(f"**🤖 AI:** {msg}")
