from typing import Literal
from langchain_core.messages import SystemMessage
from langgraph.graph import START,END,MessagesState,StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import InMemorySaver

from ai.llm import llm
from ai.prompts import COPILOT_SYSTEM_PROMPT
from ai.tools import search_knowledge,create_learning_record_tool

checkpointer = InMemorySaver()

def create_copilot_graph(user_id:int):
    # 当前用户专属的学习记录工具
    learning_record_tool = create_learning_record_tool(user_id)
    tools=[search_knowledge,learning_record_tool]
    # 关键,把工具告诉模型
    model_with_tools=llm.bind_tools(tools)

    # 第一个Agent节点
    async def call_model(state:MessagesState):
        messages=[
            SystemMessage(content=COPILOT_SYSTEM_PROMPT),
            *state["messages"]
        ]
        response=await model_with_tools.ainvoke(messages)
        return {"messages":[response]}

    # conditional_edge的判断条件，是否调用工具
    def should_continue(state:MessagesState)->Literal["tools","__end__"]:
        last_message=state["messages"][-1]
        if getattr(
                last_message,
                "tool_calls",
                None
        ):
            return "tools"
        return "__end__"

    # Tool执行节点
    tool_node = ToolNode(tools)

    builder=(
        StateGraph(MessagesState)
        .add_node("agent",call_model)
        .add_node("tools",tool_node)
        .add_edge(START,"agent")
        .add_conditional_edges(
            "agent",
            should_continue,
            {
                "tools":"tools",
                "__end__":END
            }
        )
        .add_edge("tools","agent")
        .compile(checkpointer=checkpointer)
    )

    return builder