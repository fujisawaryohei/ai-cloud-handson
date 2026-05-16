from botocore.config import Config
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    SystemMessage,
    ToolCall,
    ToolMessage,
)
from langgraph.func import entrypoint, task
from langgraph.graph import add_messages

from .agent_tools import tools, tools_by_name, web_search, write_file

load_dotenv()

cfg = Config(read_timeout=300)
llm_with_tools = init_chat_model(
    model="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    model_provider="bedrock_converse",
    region_name="ap-northeast-1",
).bind_tools(tools)

system_prompt = """
あなたの責務はユーザーからのリクエストを調査し、調査結果をファイル出力する事です。
- ユーザーのリクエスト調査にWeb検索が必要であれば、Web検索ツールを使ってください。
- 必要な情報が集まったと判断したら検索は終了して下さい。
- 検索は最大2回までとしてください。
- ファイル出力はmarkdown形式(.md)に変換して保存してください。
・Web検索が拒否された場合、Web検索を中止してください。
・レポート保存が拒否された場合、レポート作成を中止し、内容をユーザーに直接つたえてください。
"""


@task
def invoke_llm(messages: list[BaseMessage]) -> AIMessage:
    response = llm_with_tools.invoke([SystemMessage(content=system_prompt)] + messages)
    return response


@task
def use_tool(tool_call):
    tool = tools_by_name[tool_call["name"]]
    observation = tool.invoke(tool_call["args"])
    return ToolMessage(content=observation, tool_call_id=tool_call["id"])


def ask_human(tool_call: ToolCall):
    tool_name = tool_call["name"]
    tool_args = tool_call["args"]

    print("\n--- ツール実行の承認 ---")
    if tool_name == web_search.name:
        print(f"ツール名: {tool_name}")
        for key, value in tool_args.items():
            print(f"  {key}: {value}")
    elif tool_name == write_file.name:
        print(f"ツール名: {tool_name}")
        print(f"保存ファイル名: {tool_args['file_path']}")

    feedback = input("承認しますか？ [APPROVE/REJECT]: ").strip()

    if feedback == "APPROVE":
        return tool_call

    return ToolMessage(
        content="ツール利用が拒否されたため、処理を終了してください。",
        name=tool_name,
        tool_call_id=tool_call["id"],
    )


@entrypoint()
def agent(messages: list[BaseMessage]):
    llm_response = invoke_llm(messages).result()
    print(f"\n[LLM] 初回応答: {llm_response.content or '(ツール呼び出し)'}")

    while True:
        if not llm_response.tool_calls:
            break

        approved_tools = []
        tool_results = []

        for tool_call in llm_response.tool_calls:
            feedback = ask_human(tool_call)
            if isinstance(feedback, ToolMessage):
                print(f"[Human] 拒否: {tool_call['name']}")
                tool_results.append(feedback)
            else:
                print(f"[Human] 承認: {tool_call['name']}")
                approved_tools.append(feedback)

        tool_futures = []
        for tool_call in approved_tools:
            future = use_tool(tool_call)
            tool_futures.append(future)

        tool_use_results = []
        for future in tool_futures:
            result = future.result()
            print(f"\n[Tool] 実行結果: {str(result.content)[:200]}")
            tool_use_results.append(result)

        messages = add_messages(
            messages, [llm_response, *tool_use_results, *tool_results]
        )

        llm_response = invoke_llm(messages).result()
        print(f"\n[LLM] 再呼び出し応答: {llm_response.content or '(ツール呼び出し)'}")

    print(f"\n[完了] 最終回答:\n{llm_response.content}")
    return llm_response


if __name__ == "__main__":
    config = {"configurable": {"thread_id": "1"}}
    user_input = input("リクエストを入力してください: ")
    agent.invoke([{"role": "user", "content": user_input}], config=config)
