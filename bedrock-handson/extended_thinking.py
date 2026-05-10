import boto3

client = boto3.client("bedrock-runtime", region_name="ap-northeast-1")

response = client.converse(
    modelId="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    messages=[{"role": "user", "content": [{"text": "こんにちは"}]}],
    additionalModelRequestFields={
        "thinking": {"type": "enabled", "budget_tokens": 1024}
    },
)

for content in response["output"]["message"]["content"]:
    if "reasoningContent" in content:
        print("<thinking>")
        print(content["reasoningContent"]["reasoningText"]["text"])
        print("</thinking>")
    elif "text" in content:
        print(content["text"])
