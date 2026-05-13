import asyncio

from agent_state import AgentState
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode
from mcp_tools import tools
from node.agent_node import agent


def route_node(state: AgentState):
    last_message = state.messages[-1]
    if not isinstance(last_message, AIMessage):
        raise ValueError(
            "[AIMessage]以外のメッセージです。遷移が不正な可能性があります。"
        )
    if not last_message.tool_calls:
        return END
    return "tools"


async def main():
    mcp_tools = await tools()

    builder = StateGraph(AgentState)

    builder.add_node("agent", agent)
    builder.add_node("tools", ToolNode(mcp_tools))

    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", route_node)
    builder.add_edge("tools", "agent")

    graph = builder.compile(name="React Agent")

    question = "Bedrockで利用可能なモデルプロバイダーを教えて!"
    response = await graph.ainvoke({"messages": [HumanMessage(question)]})

    return response


if __name__ == "__main__":
    response = asyncio.run(main())
    print(response)
