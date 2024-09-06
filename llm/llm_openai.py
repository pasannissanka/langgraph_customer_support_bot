from langchain_openai import ChatOpenAI
from data.configs import Configs


configs = Configs()

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    api_key=configs.OPEN_AI_API_KEY
)
