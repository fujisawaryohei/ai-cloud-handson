import os
from typing import Dict, List

import boto3
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, SystemMessage
from langchain_core.tools import tool
from langchain_tavily import TavilySearch

from investigation_agent.agent_state import AgentState

load_dotenv()

web_search = TavilySearch(max_results=2)


@tool
def send_aws_sns(text: str):
    """テキストをAWS SNSトピックにPublishするツール"""
    topic_arn = os.getenv("SNS_TOPIC_ARN")
    sns_client = boto3.client("sns", region_name="ap-northeast-1")
    sns_client.publish(TopicArn=topic_arn, Message=text)


tools = [web_search, send_aws_sns]

model = init_chat_model(
    model="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    model_provider="bedrock_converse",
    region_name="ap-northeast-1",
).bind_tools(tools)

system_prompt = """
あなたの責務はユーザーからの質問を調査し、結果を要約してAWS SNSにお送る事です。
検索は1回のみとしてください。
"""


async def agent(state: AgentState) -> Dict[str, List[AIMessage]]:
    # responseにはAIMessageが返る
    # messagesには、Annotated[List[AnyMessage], operator.add] で、常にMessageがAppendされるようになっている。
    # つまり、やり取りが履歴化するようになっている。
    # 常に履歴を維持しつつ、system_promptを頭に渡すようにするために、以下のような渡し方になっている。
    response = await model.ainvoke([SystemMessage(system_prompt)] + state.messages)
    return {"messages": [response]}
