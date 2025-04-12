import asyncio
from dataclasses import asdict
from mcphub import MCPHub  # Import MCPHub from mcphub.py
from agents.mcp import MCPServerStdio
import json

# Create an instance of MCPHub, which automatically loads the configuration
mcphub = MCPHub()
# sequential_thinking_server = mcphub.fetch_server_params("azure-storage-mcp")

# print(f"Using MCP server: {sequential_thinking_server}")

async def main():
    async with mcphub.fetch_openai_mcp_server(
        cache_tools_list=True,  # Cache the tools list, for demonstration
        mcp_name="azure-storage-mcp",  # Use the MCP server configuration
    ) as server:
        tools = await server.list_tools()
        tools_dict = [
            dict(tool) if hasattr(tool, "__dict__") else tool for tool in tools
        ]
        print("Tools available:")
        print(json.dumps(tools_dict, indent=2))

if __name__ == "__main__":
    asyncio.run(main())