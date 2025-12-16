import streamlit as st
import requests
import os

st.set_page_config(
    page_title="M-NeuraChat",
    page_icon="",
    layout="centered"
)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "google/gemma-3n-e4b-it:free"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

st.markdown("""
<style>
/* ===== Global ===== */
html, body, [class*="css"] {
    font-family: 'Segoe UI', system-ui, sans-serif;
    background-color: #000000;
    color: #e5e5e5;
}

/* Remove Streamlit default background */
.stApp {
    background-color: #000000;
}

/* ===== Header ===== */
.header {
    background-color: #000000;
    padding: 24px;
    border-radius: 12px;
    text-align: center;
    margin-bottom: 20px;
    border: 1px solid #262626;
}

.header h1 {
    margin: 0;
    font-size: 2.2rem;
    color: #ffffff;
    font-weight: 600;
}

.header p {
    margin-top: 6px;
    color: #a3a3a3;
    font-size: 0.95rem;
}

/* ===== Chat Container ===== */
.chat-box {
    background-color: #000000;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #262626;
}

/* ===== Sidebar ===== */
section[data-testid="stSidebar"] {
    background-color: #000000;
    border-right: 1px solid #262626;
}

section[data-testid="stSidebar"] * {
    color: #e5e5e5;
}

/* Sidebar buttons */
section[data-testid="stSidebar"] button {
    background-color: #ffffff;
    color: #000000;
    border-radius: 10px;
    font-weight: 500;
}

section[data-testid="stSidebar"] button:hover {
    background-color: #e5e5e5;
}

/* ===== Chat Input ===== */
div[data-testid="stChatInput"] textarea {
    background-color: #0a0a0a;
    color: #ffffff;
    border-radius: 12px;
    padding: 12px;
    border: 1px solid #262626;
}

div[data-testid="stChatInput"] textarea::placeholder {
    color: #737373;
}

/* ===== Chat Messages ===== */
div[data-testid="stChatMessage"] {
    background-color: #000000;
    border-radius: 12px;
    padding: 10px;
    border: 1px solid #262626;
    margin-bottom: 10px;
}

/* User message */
div[data-testid="stChatMessage"][data-role="user"] {
    background-color: #0a0a0a;
}

/* Assistant message */
div[data-testid="stChatMessage"][data-role="assistant"] {
    background-color: #000000;
}

/* Code blocks */
pre {
    background-color: #0a0a0a !important;
    border-radius: 10px;
    padding: 12px;
    border: 1px solid #262626;
}

/* Scrollbar (optional, clean look) */
::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-thumb {
    background: #262626;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header">
    <h1>MChatbot</h1>
    <p>Powered by OpenRouter • Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header(" Settings")
    st.markdown("**Model in use**")
    st.code(MODEL)

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("<small>Developed by Mayur</small>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.container():
    st.markdown('<div class="chat-box">', unsafe_allow_html=True)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    st.markdown('</div>', unsafe_allow_html=True)

user_input = st.chat_input("Ask anything...")

def get_ai_response(messages):
    try:
        response = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": messages
            },
            timeout=30
        )

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        return f" API Error ({response.status_code})"

    except requests.exceptions.Timeout:
        return "⏱Request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        return f" Network error: {str(e)}"

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = get_ai_response(st.session_state.messages)
            st.markdown(reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

