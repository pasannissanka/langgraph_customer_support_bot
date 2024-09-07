import uuid

import streamlit as st
import random
import time

from langchain_core.messages import ToolMessage

from data.configs import Configs
from data.vector_store import VectorStore
from data.db import DB
from agents.graph import graph
from utils.helpers import print_event


def app():
    configs = Configs()
    db = DB()
    vector_store = None

    st.title("Simple chat")
    try:
        st.image(graph.get_graph(xray=True).draw_mermaid_png())
    except Exception:
        # This requires some extra dependencies and is optional
        pass

    with st.sidebar:
        if configs.OPEN_AI_API_KEY is None:
            OPEN_AI_KEY = st.text_input("OpenAI API Key", key="keys_open_ai_key", type="password")
            "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
            configs.set_open_ai_key(openai_api_key=OPEN_AI_KEY)
        if configs.LANGCHAIN_API_KEY is None:
            LANGCHAIN_API_KEY = st.text_input("Langchain API Key", key="keys_langchain_api_key_", type="password")
            "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
            configs.set_langchain_api_key(langchain_api_key=LANGCHAIN_API_KEY)

    if configs.OPEN_AI_API_KEY is not None:
        vector_store = VectorStore()

    thread_id = str(uuid.uuid4())
    config = {
        "configurable": {
            # The passenger_id is used in our flight tools to
            # fetch the user's flight information
            "passenger_id": "3442 587242",
            # Checkpoints are accessed by thread_id
            "thread_id": thread_id,
        }
    }

    # Initialize chat history
    _printed = set()
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

        # Stream agent's response and events using the user's prompt
        events = graph.stream(
            {"messages": ("user", prompt)}, config, stream_mode="values"
        )
        for event in events:
            current_state = event.get("dialog_state")
            if current_state:
                print("Currently in: ", current_state[-1])
            message = event.get("messages")
            if message:
                print(f"Message: {message}")
                if isinstance(message, list):
                    message = message[-1]
                if message.id not in _printed:
                    msg_repr = message.pretty_repr(html=True)
                    _printed.add(message.id)

                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": msg_repr})
                    with st.chat_message("assistant"):
                        st.markdown(msg_repr)

        snapshot = graph.get_state(config)
        while snapshot.next:
            # Handle interrupt and user input approval
            user_input = st.text_input(
                "Do you approve of the above actions? Type 'y' to continue, otherwise explain your requested changes."
            )
            if user_input.strip() == "y":
                result = graph.invoke(None, config)
            else:
                result = graph.invoke(
                    {
                        "messages": [
                            ToolMessage(
                                tool_call_id=event["messages"][-1].tool_calls[0]["id"],
                                content=f"API call denied by user. Reason: '{user_input}'. Continue assisting, "
                                        f"accounting for the user's input.",
                            )
                        ]
                    },
                    config,
                )
            snapshot = graph.get_state(config)
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(result)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": result})


if __name__ == '__main__':
    app()
