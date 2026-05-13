from typing import List
from langchain_mcp_adapters.client import MultiServerMCPClient, BaseTool


async def tools() -> List[BaseTool]:
    client = MultiServerMCPClient(
        {
            "file-system": {
                "command": "npx",
                "args": [
                    "-y",
                    "@modelcontextprotocol/server-filesystem@2025.7.1",
                    "./",
                ],
                "transport": "stdio",
            },
            "aws-knowledge-mcp-server": {
                "url": "https://knowledge-mcp.global.api.aws",
                "transport": "streamable_http",
            },
        }
    )

    mcp_tools = await client.get_tools()
    return mcp_tools
