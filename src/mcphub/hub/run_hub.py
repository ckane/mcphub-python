import asyncio
from mcphub.hub.utilities import setup_all_servers, store_mcp, list_servers, list_tools


async def main():
    # Setup all MCP servers
    await setup_all_servers()

    # Store MCP server and tool data in MongoDB
    await store_mcp()

    # Display stored servers and tools
    servers = list_servers()
    print("\nStored Servers:")
    for server in servers:
        print(f"Server: {server.name}")
        print(f"Description: {server.description}")
        print(f"Tags: {', '.join(server.tags)}")
        print(f"Command: {server.command}")

    tools = await list_tools()
    print("\nTools:")
    for server_name, server_tools in tools.items():
        print(f"Server: {server_name}")
        for tool in server_tools:
            print(f"Tool: {tool.name}")
            print(f"Description: {tool.description}")
            print()


if __name__ == "__main__":
    asyncio.run(main())
