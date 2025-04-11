"""Command-line interface for MCPHub."""

import asyncio
import argparse
import json
from pathlib import Path
from mcphub.hub.utilities import setup_all_servers, store_mcp, list_tools
from mcphub.hub.mcp_server_config import list_servers
from mcphub.adapter.adapter import MCPHubAdapter


def setup_parser():
    """Set up the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        description="MCPHub - A hub for Model Context Protocol (MCP) servers"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Setup command
    setup_parser = subparsers.add_parser("setup", help="Set up MCP servers")
    
    # List servers command
    list_servers_parser = subparsers.add_parser("list-servers", help="List available MCP servers")
    
    # List tools command
    list_tools_parser = subparsers.add_parser("list-tools", help="List tools from MCP servers")
    list_tools_parser.add_argument("--server", help="Filter tools by server name")
    list_tools_parser.add_argument("--json", action="store_true", help="Output in JSON format")
    
    # Run adapter command
    adapter_parser = subparsers.add_parser("adapter", help="Run the MCPHubAdapter")
    adapter_parser.add_argument(
        "--config", 
        default="mcp_config.yaml", 
        help="Path to the configuration file"
    )
    adapter_parser.add_argument(
        "--cache", 
        default="cache", 
        help="Path to the cache directory"
    )
    adapter_parser.add_argument(
        "--server", 
        required=True,
        help="Server type to use"
    )
    
    return parser


async def run_setup():
    """Set up all MCP servers."""
    await setup_all_servers()
    await store_mcp()
    print("✅ All MCP servers have been set up successfully")


async def run_list_servers():
    """List all available servers."""
    servers = list_servers()
    print("\nAvailable MCP Servers:")
    for server in servers:
        print(f"  • {server.name}")
        print(f"    Description: {server.description}")
        print(f"    Tags: {', '.join(server.tags) if server.tags else 'None'}")
        print()


async def run_list_tools(server_name=None, json_output=False):
    """List tools from MCP servers."""
    tools_by_server = await list_tools()
    
    if server_name:
        if server_name in tools_by_server:
            tools = {server_name: tools_by_server[server_name]}
        else:
            print(f"❌ Server '{server_name}' not found")
            return
    else:
        tools = tools_by_server
    
    if json_output:
        print(json.dumps(tools, indent=2, default=lambda o: o.__dict__))
    else:
        print("\nMCP Tools:")
        for server, server_tools in tools.items():
            print(f"\n📦 Server: {server}")
            if not server_tools:
                print("  No tools available")
                continue
                
            for tool in server_tools:
                print(f"  • {tool.name}")
                print(f"    Description: {tool.description}")
                print()


async def run_adapter(config_path, cache_path, server_type):
    """Run the MCPHubAdapter with the specified configuration."""
    try:
        adapter = MCPHubAdapter().from_config(config_path, cache_path=cache_path)
        server_config = adapter.get_server(server_type)
        
        if server_config:
            print(f"✅ Successfully loaded server config: {server_config.name}")
            print(f"  Command: {server_config.command} {' '.join(server_config.args)}")
            print(f"  Description: {server_config.description or 'N/A'}")
        else:
            print(f"❌ Server '{server_type}' not found in configuration")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


async def run_command(args):
    """Run the specified command."""
    if args.command == "setup":
        await run_setup()
    elif args.command == "list-servers":
        await run_list_servers()
    elif args.command == "list-tools":
        await run_list_tools(args.server, args.json)
    elif args.command == "adapter":
        await run_adapter(args.config, args.cache, args.server)
    else:
        print("Please specify a command. Use --help for available commands.")


def main():
    """Entry point for the CLI."""
    parser = setup_parser()
    args = parser.parse_args()
    
    if hasattr(args, "command") and args.command:
        asyncio.run(run_command(args))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
