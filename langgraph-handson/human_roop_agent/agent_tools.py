from dotenv import load_dotenv
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_tavily import TavilySearch

load_dotenv()

web_search = TavilySearch(max_results=2, topic="general")

working_directory = "report"

file_toolkit = FileManagementToolkit(
    root_dir=str(working_directory),
    selected_tools=["write_file"],
)
write_file = file_toolkit.get_tools()[0]

tools = [web_search, write_file]
tools_by_name = {tool.name: tool for tool in tools}
