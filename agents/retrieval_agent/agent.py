from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate
from llm.llm_openai import llm
from utils.complete_or_escalate import CompleteOrEscalate
from agents.retrieval_agent.tools import lookup_policy

retrival_assistant_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a customer service chatbot."
            "Your primary role is to search for product information and answer."
            " If a search comes up empty, expand your search before giving up."
            "\nCurrent time: {time}.",
            "\n\nIf the user needs help, and none of your tools are appropriate for it, then"
            ' "CompleteOrEscalate" the dialog to the host assistant. Do not waste the user\'s time. Do not make up '
            'invalid tools or functions.',
        ),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now())
retrival_assistant_tools = [
    lookup_policy,
]

retrival_runnable = retrival_assistant_prompt | llm.bind_tools(
    [CompleteOrEscalate]
)
