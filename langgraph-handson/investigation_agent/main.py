import asyncio

from langchain_core.messages import HumanMessage
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode

from investigation_agent.agent_state import AgentState
from investigation_agent.node.agnet_node import agent, tools


def route_node(state: AgentState):
    last_message = state.messages[-1]
    if not last_message.tool_calls:
        return END
    return "tools"

builder = StateGraph(AgentState)

builder.add_node(agent)
builder.add_node(ToolNode(tools))

builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", route_node)
builder.add_edge("tools", "agent")

graph = builder.compile()


async def main():
    question = "LangGraphの基本をやさしく教えて"
    response = await graph.ainvoke({"messages": [HumanMessage(question)]})
    return response


if __name__ == "__main__":
    response = asyncio.run(main())
    print(response)

