import streamlit as st

from utils import get_chat_response
from langchain.memory import ConversationBufferMemory
from openai import AuthenticationError

st.title("Chatbot")

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    st.markdown("[OpenA API Key](https://platform.openai.com/account)")

if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(return_messages=True)
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hello! How can I assist you today?"},
    ]

for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input()

if prompt:
    if not openai_api_key:
        st.info("Please enter your OpenAI API key.")
        st.stop()
    st.session_state["messages"].append({"role": "human", "content": prompt})
    st.chat_message("human").write(prompt)

    try:
        with st.spinner("Thinking..."):
            response = get_chat_response(
                prompt, st.session_state["memory"], openai_api_key
            )
            msg = {"role": "assistant", "content": response}
            st.session_state["messages"].append(msg)
            st.chat_message("assistant").write(response)
    except AuthenticationError:
        st.error("Invalid OpenAI API key. Please check and try again.")
        st.stop()
