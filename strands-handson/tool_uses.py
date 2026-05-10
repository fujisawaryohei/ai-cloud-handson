import feedparser
from strands import Agent, tool
from strands.models import BedrockModel


@tool
def get_aws_update(service_name: str) -> list:
    feed = feedparser.parse("https://aws.amazon.com/about-aws/whats-new/recent/feed/")
    result = []

    for entry in feed.entries:
        if service_name.lower() in entry.title.lower():
            result.append(
                {
                    "published": entry.get("published", "N/A"),
                    "summary": entry.get("summary", ""),
                }
            )

            if len(result) >= 3:
                break
    return result


model = BedrockModel(
    model_id="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    region_name="ap-northeast-1",
)
agent = Agent(model=model, tools=[get_aws_update])

service_name = input("アップデートを知りたいAWSサービス名を入力してください。")
prompt = f"AWSの{service_name}の最新アップデートを、日付つきで要約して。"

agent(prompt)
