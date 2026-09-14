from langchain_core.output_parsers import StrOutputParser

from ai.llm import llm
from ai.prompts import chat_prompt

chat_chain=(
    chat_prompt | llm | StrOutputParser()
)