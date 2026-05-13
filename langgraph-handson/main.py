from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage

model = init_chat_model(
    model="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    model_provider="bedrock_converse",
    region_name="ap-northeast-1",
)

messages = [
    HumanMessage("日本の首都は？"),
    AIMessage("東京です。"),
    HumanMessage("聞こえなかったので、もう一回言って？"),
]

response = model.stream(messages)

for chunk in response:
    print(chunk.content, end="", flush=True)
