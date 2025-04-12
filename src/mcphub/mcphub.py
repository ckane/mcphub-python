from dataclasses import dataclass, field
from pathlib import Path
from typing import AsyncGenerator, Optional

from agents.mcp import MCPServerStdio
from mcp import StdioServerParameters
from mcp_servers import MCPServerConfig, MCPServers, MCPServersParams


@dataclass
class MCPHub:
    servers_params: MCPServersParams = field(init=False)

    def __post_init__(self):
        config_path = self._find_config_path()
        self.servers_params = MCPServersParams(config_path)
        self.servers = MCPServers(self.servers_params)

    def _find_config_path(self) -> str:
        current_dir = Path.cwd()
        for parent in [current_dir] + list(current_dir.parents):
            config_path = parent / ".mcphub.json"
            if config_path.exists():
                return str(config_path)
        raise FileNotFoundError("Configuration file '.mcphub.json' not found in the project root or any parent directories.")

    def fetch_server_params(self, mcp_name: str) -> Optional[MCPServerConfig]:
        return self.servers_params.retrieve_server_params(mcp_name)
    
    def fetch_stdio_server_config(self, mcp_name: str) -> Optional[StdioServerParameters]:
        return self.servers_params.convert_to_stdio_params(mcp_name)
    
    def fetch_openai_mcp_server(self, mcp_name: str, cache_tools_list: bool = True) -> MCPServerStdio:
        """
        Fetch and return an OpenAI MCP server instance.
        
        Args:
            mcp_name: The name of the MCP server to fetch
            cache_tools_list: Whether to cache the tools list
            
        Returns:
            MCPServerStdio: The configured MCP server
        """
        return self.servers.make_openai_mcp_server(mcp_name, cache_tools_list)