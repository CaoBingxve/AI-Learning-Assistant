import os

from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek


load_dotenv()


API_KEY = os.getenv("DEEPSEEK_API_KEY")
MODEL_NAME = os.getenv(
    "DEEPSEEK_MODEL",
    "deepseek-chat"
)


llm = ChatDeepSeek(
    model=MODEL_NAME,
    api_key=API_KEY,
    temperature=0.3
)