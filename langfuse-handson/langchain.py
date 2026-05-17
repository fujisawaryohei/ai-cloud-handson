from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langfuse.langchain import CallbackHandler

load_dotenv()

model = init_chat_model(
    model="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    model_provider="bedrock_converse",
    region_name="ap-northeast-1",
)

langfuse_handler = CallbackHandler()
config = {"callbacks": [langfuse_handler]}

response = model.invoke("こんにちは", config)
print(response.content)
