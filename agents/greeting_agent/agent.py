from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate
from llm.llm_openai import llm
from utils.complete_or_escalate import CompleteOrEscalate

# Define the Greeting Agent
greeting_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a customer service chatbot. Greet the user warmly and ask how you can assist them today."
            " The primary assistant delegates work to you whenever the user needs introduction"
            "When searching, be persistent. Expand your query bounds if the first search returns no results. "
            "If you need more information or the customer changes their mind, escalate the task back to the main "
            "assistant."
            "\nCurrent time: {time}."
            "\n\nIf the user needs help, and none of your tools are appropriate for it, then"
            ' "CompleteOrEscalate" the dialog to the host assistant. Do not waste the user\'s time. Do not make up '
            'invalid tools or functions.',
        ),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now())

greeting_runnable = greeting_prompt | llm.bind_tools(
    [CompleteOrEscalate]
)
