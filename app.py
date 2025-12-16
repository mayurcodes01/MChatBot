import streamlit as st
import os
from google import genai

# ================== Page Config ==================
st.set_page_config(
    page_title="M-NeuraChat",
    page_icon="🤖",
    layout="centered"
)

# ================== Gemini Client ==================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("GEMINI_API_KEY not found. Set it as an environment variable.")
    st.stop()

client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-2.5-flash"

# ================== Styles ==================
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Segoe UI', system-ui, sans-serif;
    background-color: #000000;
    color: #e5e5e5;
}

.stApp {
    background-color: #000000;
}

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

.chat-box {
    background-color: #000000;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #262626;
}

section[data-testid="stSidebar"] {
    background-color: #000000;
    border-right: 1px solid #262626;
}

section[data-testid="stSidebar"] button {
    background-color: #ffffff !important;
    color: #000000 !important;
    border-radius: 10px;
    font-weight: 500;
    border: none;
}

section[data-testid="stSidebar"] button svg {
    fill: #000000 !important;
}

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

div[data-testid="stChatMessage"] {
    background-color: #000000;
    border-radius: 12px;
    padding: 10px;
    border: 1px solid #262626;
    margin-bottom: 10px;
}

div[data-testid="stChatMessage"][data-role="user"] {
    background-color: #0a0a0a;
}

pre {
    background-color: #0a0a0a !important;
    border-radius: 10px;
    padding: 12px;
    border: 1px solid #262626;
}

::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-thumb {
    background: #262626;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ================== Header ==================
st.markdown("""
<div class="header">
    <h1>M-NeuraChat</h1>
    <p>Powered by Google Gemini • Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)

# ================== Sidebar ==================
with st.sidebar:
    st.header(" Settings")
    st.markdown("**Model in use**")
    st.code(MODEL_NAME)

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("""
<small>
Developed by Mayur<br>
<a href="https://github.com/mayurcodes01" target="_blank"
style="color:#a3a3a3; text-decoration:none;">
GitHub Repository
</a>
</small>
""", unsafe_allow_html=True)

# ================== Chat State ==================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ================== Display Messages ==================
with st.container():
    st.markdown('<div class="chat-box">', unsafe_allow_html=True)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    st.markdown('</div>', unsafe_allow_html=True)

# ================== Gemini Response Function ==================
def get_ai_response(messages):
    try:
        contents = []
        for m in messages:
            contents.append({
                "role": m["role"],
                "parts": [{"text": m["content"]}]
            })

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents
        )
        return response.text

    except Exception as e:
        return f"Error: {str(e)}"

# ================== User Input ==================
user_input = st.chat_input("Ask anything...")

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
