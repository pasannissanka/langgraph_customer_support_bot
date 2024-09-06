import streamlit as st
import random
import time

from data.configs import Configs
from data.vector_store import VectorStore


# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


configs = Configs()
vector_store = VectorStore()


def app():
    with st.sidebar:
        if configs.OPEN_AI_API_KEY is None:
            OPEN_AI_KEY = st.text_input("OpenAI API Key", key="keys_open_ai_key", type="password")
            "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
            configs.set_open_ai_key(openai_api_key=OPEN_AI_KEY)
        if configs.LANGCHAIN_API_KEY is None:
            LANGCHAIN_API_KEY = st.text_input("Langchain API Key", key="keys_langchain_api_key_", type="password")
            "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
            configs.set_langchain_api_key(langchain_api_key=LANGCHAIN_API_KEY)

    st.title("Simple chat")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = st.write_stream(response_generator())
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == '__main__':
    app()
