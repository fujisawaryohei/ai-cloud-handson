from typing import Dict, List

from agent_state import AgentState
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, SystemMessage
from langchain_core.runnables import Runnable
from mcp_tools import tools


async def initialize_model() -> Runnable:
    mcp_tools = await tools()

    for t in mcp_tools:
        getattr(t, "args_schema", {})["type"] = "object"

    model = init_chat_model(
        model="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
        model_provider="bedrock_converse",
        region_name="ap-northeast-1",
    ).bind_tools(mcp_tools)

    return model


system_prompt = """
あなたの責務はAWSドキュメントを検索し、Markdown形式としてファイル出力することです。
- 検索後、Markdown形式に変換してください。
- 検索は最大で2回までとし、その時点での情報を出力してください。
"""


async def agent(state: AgentState) -> Dict[str, List[AIMessage]]:
    model = await initialize_model()
    response = await model.ainvoke([SystemMessage(system_prompt)] + state.messages)
    return {"messages": [response]}
