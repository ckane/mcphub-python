import asyncio
from dataclasses import asdict  # Add this import
from adapter import MCPHubAdapter
from agents import Agent, Runner, trace
from agents.mcp import MCPServer, MCPServerStdio
import json

adapter = MCPHubAdapter().from_config("mcp_config.yaml", cache_path="cache")
azure_devops_server = adapter.get_server("azure-devops-mcp")

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
