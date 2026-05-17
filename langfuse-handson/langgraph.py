from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_tavily import TavilySearch
from langfuse import get_client
from langfuse.langchain import CallbackHandler
from langgraph.prebuilt import create_react_agent

load_dotenv()

langfuse = get_client()

# langfuse.create_prompt(
#     name="ai-agent",
#     type="chat",
#     prompt=[{"role": "user", "content": "{{city}}の人口は？"}],
#     config={"model": "jp.anthropic.claude-haiku-4-5-20251001-v1:0", "temperature": 1},
# )

web_search = TavilySearch(max_results=2, topic="general")

tools = [web_search]

llm = init_chat_model(
    model="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    model_provider="bedrock_converse",
    region_name="ap-northeast-1",
)
agent = create_react_agent(llm, tools)
langfuse_handler = CallbackHandler()

prompt_template = langfuse.get_prompt(name="ai-agent", type="chat", label="latest")
langchain_prompt = ChatPromptTemplate(prompt_template.get_langchain_prompt())
prompt = langchain_prompt.invoke({"city": "横浜"})

messages = agent.invoke(
    {"messages": prompt.to_messages()},
    config={"callbacks": [langfuse_handler]},
)

for message in messages["messages"]:
    message.pretty_print()
