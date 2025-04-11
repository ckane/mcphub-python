from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from mcp_servers import MCPServerConfig, MCPServersParams


@dataclass
class MCPHub:
    servers_params: MCPServersParams = field(init=False)

    def __post_init__(self):
        config_path = self._find_config_path()
        self.servers_params = MCPServersParams(config_path)

    def _find_config_path(self) -> str:
        current_dir = Path.cwd()
        for parent in [current_dir] + list(current_dir.parents):
            config_path = parent / ".mcphub.yaml"
            if config_path.exists():
                return str(config_path)
        raise FileNotFoundError("Configuration file '.mcphub.yaml' not found in the project root or any parent directories.")

    def get_server(self, mcp_name: str) -> Optional[MCPServerConfig]:
        return self.servers_params.get_server_params(mcp_name)