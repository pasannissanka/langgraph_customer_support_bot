import os

from dotenv import load_dotenv

from utils.decorators import singleton

load_dotenv()


@singleton
class Configs:
    def __init__(self):
        self.OPEN_AI_API_KEY = os.getenv('OPENAI_API_KEY')
        self.LANGCHAIN_API_KEY = os.getenv('LANGCHAIN_API_KEY')

    def set_open_ai_key(self, openai_api_key):
        self.OPEN_AI_API_KEY = openai_api_key

    def set_langchain_api_key(self, langchain_api_key):
        self.LANGCHAIN_API_KEY = langchain_api_key
