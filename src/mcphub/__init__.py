"""
MCPHub - A hub for Model Context Protocol (MCP) servers.

This package provides tools for managing and interacting with MCP servers.
"""

__version__ = "0.1.0"

from mcphub.adapter.adapter import MCPHubAdapter, MCPServerConfig
from mcphub.hub.mcp_hub import setup_all_servers, store_mcp, list_tools
from mcphub.hub.mcp_controller import list_servers, get_server
