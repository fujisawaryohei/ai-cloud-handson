import boto3

client = boto3.client("bedrock-runtime", region_name="ap-northeast-1")

response = client.converse(
    modelId="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    messages=[{"role": "user", "content": [{"text": "こんにちは"}]}],
    inferenceConfig={"maxTokens": 1024},
)

print(response["output"]["message"]["content"][0]["text"])
