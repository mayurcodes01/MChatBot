import streamlit as st
import requests
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="Mayur AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "google/gemma-3n-e4b-it:free"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

st.markdown(
    """
    <h1 style="text-align:center;"> Mayur's AI Chatbot</h1>
    <p style="text-align:center; color:gray;">
    Powered by OpenRouter • Built with Streamlit
    </p>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    st.header("Settings")
    st.markdown("Model in use:")
    st.code(MODEL)
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown(
        "<small>Developed by Mayur</small>",
        unsafe_allow_html=True
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask anything...")

def get_ai_response(messages):
    """Send request to OpenRouter API and return response text"""
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
        else:
            return f" API Error ({response.status_code})"

    except requests.exceptions.Timeout:
        return "⏱️ Request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        return f" Network error: {str(e)}"

if user_input:
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Assistant typing indicator
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = get_ai_response(st.session_state.messages)
            st.markdown(reply)

    # Save assistant reply
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })
