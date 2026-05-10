from strands import Agent
from strands.models import BedrockModel

model = BedrockModel(
    model_id="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    region_name="ap-northeast-1",
)

agent = Agent(model=model)
agent("Strandsってどういう意味？")