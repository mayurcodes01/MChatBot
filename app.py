import streamlit as st
import requests
import os

st.set_page_config(
    page_title="MNeuron",
    
    layout="centered"
)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "google/gemma-3n-e4b-it:free"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

st.markdown("""
<style>
/* Global */
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

/* Header */
.header {
    background: linear-gradient(135deg, #4f46e5, #9333ea);
    padding: 20px;
    border-radius: 16px;
    color: white;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
}

.header h1 {
    margin: 0;
    font-size: 2.2rem;
}

.header p {
    margin-top: 5px;
    opacity: 0.85;
}

/* Chat container */
.chat-box {
    background-color: #f9fafb;
    padding: 15px;
    border-radius: 16px;
    box-shadow: inset 0 0 0 1px #e5e7eb;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0f172a;
}

section[data-testid="stSidebar"] * {
    color: #e5e7eb;
}

section[data-testid="stSidebar"] button {
    background-color: #6366f1;
    color: white;
    border-radius: 10px;
}

/* Chat input */
div[data-testid="stChatInput"] textarea {
    border-radius: 14px;
    padding: 12px;
}

/* Chat bubbles */
div[data-testid="stChatMessage"] {
    border-radius: 14px;
    padding: 8px;
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
import streamlit as st
import requests
import os

st.set_page_config(
    page_title="MNeuron",
    page_icon="",
    layout="centered"
)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "google/gemma-3n-e4b-it:free"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

st.markdown("""
<style>
/* Global */
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

/* Header */
.header {
    background: linear-gradient(135deg, #4f46e5, #9333ea);
    padding: 20px;
    border-radius: 16px;
    color: white;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
}

.header h1 {
    margin: 0;
    font-size: 2.2rem;
}

.header p {
    margin-top: 5px;
    opacity: 0.85;
}

/* Chat container */
.chat-box {
    background-color: #f9fafb;
    padding: 15px;
    border-radius: 16px;
    box-shadow: inset 0 0 0 1px #e5e7eb;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0f172a;
}

section[data-testid="stSidebar"] * {
    color: #e5e7eb;
}

section[data-testid="stSidebar"] button {
    background-color: #6366f1;
    color: white;
    border-radius: 10px;
}

/* Chat input */
div[data-testid="stChatInput"] textarea {
    border-radius: 14px;
    padding: 12px;
}

/* Chat bubbles */
div[data-testid="stChatMessage"] {
    border-radius: 14px;
    padding: 8px;
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

