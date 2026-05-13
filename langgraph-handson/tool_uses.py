from langchain.chat_models import init_chat_model
from langchain_core.tools import tool


@tool
def add(a: int, b: int) -> int:
    """足し算を行い、結果を返すツール"""
    return a + b


model = init_chat_model(
    model="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    model_provider="bedrock_converse",
    region_name="ap-northeast-1",
).bind_tools([add])

response = model.invoke("2と3を足すといくつになる？")
