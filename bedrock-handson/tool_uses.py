import json
import urllib.request

import boto3

client = boto3.client("bedrock-runtime", region_name="ap-northeast-1")

input = "2025年7月の祝日はいつ？"
llm = "jp.anthropic.claude-haiku-4-5-20251001-v1:0"


# 祝日を取得する関数
def get_japanese_holiday(year):
    """指定された年の日本の祝日を取得する"""
    URL = f"https://holidays-jp.github.io/api/v1/{year}/date.json"

    with urllib.request.urlopen(URL) as response:
        data = response.read()
        holidays = json.loads(data)

    return holidays


# 関数をLLMのツールとして定義
tools = [
    {
        "toolSpec": {
            "name": "get_japanese_holiday",
            "description": "指定された年の日本の祝日一覧を取得します",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "year": {
                            "type": "integer",
                            "description": "祝日を取得したい年(例: 2024)",
                        }
                    },
                    "required": ["year"],
                }
            },
        }
    }
]


# ================================
# 1回目の推論
# ================================
print("【推論1回目】")
print("ユーザーの入力: ", input)

response = client.converse(
    modelId=llm,
    messages=[{"role": "user", "content": [{"text": input}]}],
    toolConfig={"tools": tools},
)

message = response["output"]["message"]
print("LLMの回答: ", message["content"][0]["text"])

tool_use = None
for content_item in message["content"]:
    if "toolUse" in content_item:
        tool_use = content_item["toolUse"]
        print("ツール要求: ", tool_use)
        print()
        break

if tool_use:
    year = tool_use["input"]["year"]
    holiday = get_japanese_holiday(year)
    tool_result = {"year": year, "holiday": holiday, "count": len(holiday)}

    print("【アプリから直接、ツール実行して結果を取得】")
    print(tool_result)
    print()

messages = [
    {"role": "user", "content": [{"text": input}]},
    {"role": "assistant", "content": message["content"]},
    {
        "role": "user",
        "content": [
            {
                "toolResult": {
                    "toolUseId": tool_use["toolUseId"],
                    "content": [{"json": tool_result}],
                }
            }
        ],
    },
]

final_response = client.converse(
    modelId=llm, messages=messages, toolConfig={"tools": tools}
)
output = final_response["output"]["message"]["content"][0]["text"]

print("【推論2回目】")
print("ユーザーの入力: (ツールの実行結果)")
print("LLMの回答: ", output)
