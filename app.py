import streamlit as st
import requests
import json
import os

st.set_page_config(page_title="Mayur's AI Chatbot", page_icon="🤖")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "google/gemma-3n-e4b-it:free"

st.title(" AI Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        data=json.dumps({
            "model": MODEL,
            "messages": st.session_state.messages
        }, ensure_ascii=False)
    )

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
    else:
        reply = "Error connecting to AI"

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

    with st.chat_message("assistant"):
        st.markdown(reply)

