"""
MCPHub - A hub for Model Context Protocol (MCP) servers.

This package provides tools for managing and interacting with MCP servers.
"""

__version__ = "0.1.0"

from mcphub.adapter.adapter import MCPHubAdapter, MCPServerConfig
from mcphub.mcphub import MCPHub

__all__ = [
    "MCPHubAdapter",
    "MCPServerConfig",
    "MCPHub"
]
