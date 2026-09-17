from typing import Literal

from langchain_core.messages import SystemMessage

from langgraph.graph import END,START,MessagesState,StateGraph

from langgraph.prebuilt import ToolNode

from ai.llm import llm

from ai.prompts import COPILOT_SYSTEM_PROMPT

from ai.tools import create_learning_record_tool, search_knowledge

def create_copilot_graph(
    user_id: int
):

    # 当前用户专属学习记录 Tool
    learning_record_tool = (create_learning_record_tool(user_id) )

    tools = [search_knowledge,learning_record_tool,]

    # 给模型绑定工具
    model_with_tools = (llm.bind_tools(tools))

    async def call_model(
        state: MessagesState
    ):

        messages = [
            SystemMessage(content=COPILOT_SYSTEM_PROMPT),
            *state["messages"]
        ]

        response = await model_with_tools.ainvoke(messages)
        return {
            "messages": [response]
        }


    def should_continue(state: MessagesState) -> Literal["tools","__end__"]:
        last_message = (
            state["messages"][-1]
        )
        if getattr(last_message,"tool_calls",None):
            return "tools"

        return "__end__"


    tool_node = ToolNode(tools)

    graph = (
        StateGraph( MessagesState)
        .add_node( "agent",call_model)
        .add_node("tools",tool_node)
        .add_edge(START,"agent")
        .add_conditional_edges(
            "agent",
            should_continue,
            {
                "tools": "tools",
                "__end__": END
            }
        )
        .add_edge("tools","agent")
        .compile()
    )


    return graph