from langchain_core.tools import tool

from ai.rag.vector_store import retriever

from config.database import AsyncSessionLocal

from service.learning_record_service import (
    get_records_by_user as fetch_records_by_user
)


@tool
async def search_knowledge(
    query: str
) -> str:
    """
    搜索学习知识库。

    当用户的问题涉及学习资料、
    项目知识、课程笔记或知识库中的内容时，
    使用这个工具。
    """

    documents = await retriever.ainvoke(
        query
    )

    if not documents:
        return "知识库中没有找到相关资料。"

    result = []

    for document in documents:

        source = document.metadata.get(
            "source",
            "未知来源"
        )

        result.append(
            f"来源：{source}\n"
            f"内容：{document.page_content}"
        )

    return "\n\n".join(result)


def create_learning_record_tool(
    user_id: int
):

    @tool
    async def get_learning_records() -> str:
        """
        获取当前登录用户的学习记录。

        当用户询问自己的学习历史、
        最近学了什么、学习时长、
        学习进度或需要根据学习记录进行分析时，
        使用这个工具。
        """

        async with AsyncSessionLocal() as db:

            records = await fetch_records_by_user(
                db,
                user_id
            )

        if not records:
            return "当前用户暂无学习记录。"

        result = []

        for record in records:

            result.append(
                f"标题：{record.title}\n"
                f"内容：{record.content}\n"
                f"学习时长：{record.study_time}分钟\n"
                f"创建时间：{record.created_at}"
            )

        return "\n\n".join(result)

    return get_learning_records