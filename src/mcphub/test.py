import asyncio
from dataclasses import asdict
from mcphub import MCPHub  # Import MCPHub from mcphub.py
from agents.mcp import MCPServerStdio
import json

# Create an instance of MCPHub, which automatically loads the configuration
mcphub = MCPHub()
azure_devops_server = mcphub.get_server("azure-devops-mcp")

print(f"Using MCP server: {azure_devops_server}")

async def main():
    async with MCPServerStdio(
        cache_tools_list=True,  # Cache the tools list, for demonstration
        params=asdict(azure_devops_server),  # Use the MCP server configuration
    ) as server:
        tools = await server.list_tools()
        tools_dict = [
            dict(tool) if hasattr(tool, "__dict__") else tool for tool in tools
        ]
        print("Tools available:")
        print(json.dumps(tools_dict, indent=2))

if __name__ == "__main__":
    asyncio.run(main())