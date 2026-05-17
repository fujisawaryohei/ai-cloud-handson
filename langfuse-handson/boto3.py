import os

import boto3
from dotenv import load_dotenv
from langfuse import observe
from tavily import TavilyClient

load_dotenv()

bedrock_client = boto3.client("bedrock-runtime", region_name="ap-northeast-1")
model_id = "jp.anthropic.claude-haiku-4-5-20251001-v1:0"


@observe
def create_query(query):
    system_prompt = """ユーザーからの問い合わせ内容をWeb検索し、レポートを作成します。
    Web検索用のクエリを1つ作成して下さい。検索単語以外は回答しないでください。"""

    prompt = f"ユーザーの質問: {query}"

    system = [{"text": system_prompt}]
    messages = [{"role": "user", "content": [{"text": prompt}]}]

    response = bedrock_client.converse(modelId=model_id, system=system, messages=messages)

    return response["output"]["message"]["content"][0]["text"]


@observe
def web_search(query: str):
    """Get Content related the query from web."""
    tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))
    search_result = tavily_client.search(query=query, max_results=3)

    return [doc["content"] for doc in search_result["results"]]


@observe
def create_report(query: str, contents: list[str]):
    system_prompt = """Web検索した結果とクエリを元にMarkdownのレポートを作成して下さい。
    タイトルと見出しも作成してください。"""

    prompt = f"ユーザーからの質問: {query}\n\n Web検索結果: {'\n'.join(contents)}"

    system = [{"text": system_prompt}]

    messages = [{"role": "user", "content": [{"text": prompt}]}]

    response = bedrock_client.converse(
        modelId=model_id, system=system, messages=messages
    )

    return response["output"]["message"]["content"][0]["text"]


@observe
def workflow(query: str):
    web_query = create_query(query)
    contents = web_search(web_query)
    report = create_report(web_query, contents)

    return report


query = "LangGraphとLangChainのユースケースの違いについて教えてください。"

report = workflow(query)

print(report)
