from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from mcp import StdioServerParameters

from mcp_servers import MCPServerConfig, MCPServersParams, MCPServers


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