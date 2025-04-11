from dataclasses import dataclass
from typing import Dict, List, Optional
from pathlib import Path
import json
import yaml
from mcp import StdioServerParameters

@dataclass
class MCPServerConfig:
    name: str
    command: str
    args: List[str]
    env: Dict[str, str]
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    
class ServerConfigNotFoundError(Exception):
    """Raised when a server configuration is not found."""
    pass

class MCPServersParams:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self._servers_params = self._load_servers_params()

    @property
    def server_params(self) -> List[MCPServerConfig]:
        """Return the list of server parameters."""
        return list(self._servers_params.values())

    def _load_user_config(self) -> Dict:
        try:
            with open(self.config_path, "r") as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Invalid YAML in configuration file: {e}")

    def _load_predefined_servers_params(self) -> Dict:
        # Adjust the path to point to the correct location of mcphub_preconfigured_servers.json
        commands_path = Path(__file__).parent.parent / "mcphub_preconfigured_servers.json"
        if commands_path.exists():
            with open(commands_path, "r") as f:
                return json.load(f)
        return {}

    def _load_servers_params(self) -> Dict[str, MCPServerConfig]:
        config = self._load_user_config()
        predefined_servers_params = self._load_predefined_servers_params()
        servers = {}
        for mcp_name, configs in config.items():
            if len(configs) != 1:
                raise ValueError(f"Each mcp_name must have exactly one configuration. Found {len(configs)} for '{mcp_name}'.")
            server = configs[0]
            repo_name = server.get("name")
            if repo_name and predefined_servers_params.get(repo_name):
                cmd_info = predefined_servers_params[repo_name]
                servers[mcp_name] = MCPServerConfig(
                    name=repo_name,
                    command=cmd_info.get("command"),
                    args=cmd_info.get("args"),
                    env=server.get("env", {}),
                    description=cmd_info.get("description"),
                    tags=cmd_info.get("tags"),
                )
            else:
                raise ServerConfigNotFoundError(
                    f"Server '{repo_name}' not found in mcphub_preconfigured_servers.json. "
                    f"Please add command and args configuration for this server."
                )
        return servers
    
    def get_server_params(self, server_name: str) -> MCPServerConfig:
        return self._servers_params.get(server_name)