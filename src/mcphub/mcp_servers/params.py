import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from mcp import StdioServerParameters


@dataclass
class MCPServerConfig:
    package_name: str
    command: str
    args: List[str]
    env: Dict[str, str]
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    repo_url: Optional[str] = None
    setup_script: Optional[str] = None
    cwd: Optional[str] = None
    
class ServerConfigNotFoundError(Exception):
    """Raised when a server configuration is not found."""
    pass

class MCPServersParams:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self._servers_params = self._load_servers_params()

    @property
    def servers_params(self) -> List[MCPServerConfig]:
        """Return the list of server parameters."""
        return list(self._servers_params.values())

    def _load_user_config(self) -> Dict:
        """Load user configuration from JSON file."""
        try:
            with open(self.config_path, "r") as f:
                config = json.load(f)
                return config.get("mcpServers", {})
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in configuration file: {e}")

    def _load_predefined_servers_params(self) -> Dict:
        """Load predefined server parameters from JSON file."""
        commands_path = Path(__file__).parent.parent / "mcphub_preconfigured_servers.json"
        if commands_path.exists():
            with open(commands_path, "r") as f:
                return json.load(f)
        return {}

    def _load_servers_params(self) -> Dict[str, MCPServerConfig]:
        config = self._load_user_config()
        predefined_servers_params = self._load_predefined_servers_params()
        servers = {}
        
        for mcp_name, server_config in config.items():
            package_name = server_config.get("package_name")
            
            # Check if command and args are configured in user config
            if "command" in server_config and "args" in server_config:
                # Use configuration directly from .mcphub.json
                servers[mcp_name] = MCPServerConfig(
                    package_name=package_name,
                    command=server_config["command"],
                    args=server_config["args"],
                    env=server_config.get("env", {}),
                    description=server_config.get("description"),
                    tags=server_config.get("tags"),
                    repo_url=server_config.get("repo_url"),
                    setup_script=server_config.get("setup_script")
                )
            # Fallback to predefined configuration
            elif package_name and predefined_servers_params.get(package_name):
                cmd_info = predefined_servers_params[package_name]
                servers[mcp_name] = MCPServerConfig(
                    package_name=package_name,
                    command=cmd_info.get("command"),
                    args=cmd_info.get("args", []),
                    env=server_config.get("env", {}),
                    description=cmd_info.get("description"),
                    tags=cmd_info.get("tags"),
                    repo_url=cmd_info.get("repo_url"),
                    setup_script=cmd_info.get("setup_script")
                )
            else:
                raise ServerConfigNotFoundError(
                    f"Server '{package_name}' must either have command and args configured in .mcphub.json "
                    f"or be defined in mcphub_preconfigured_servers.json"
                )
        return servers
    
    def retrieve_server_params(self, server_name: str) -> MCPServerConfig:
        return self._servers_params.get(server_name)
    
    def convert_to_stdio_params(self, server_name: str) -> StdioServerParameters:
        server_params = self.retrieve_server_params(server_name)
        if not server_params:
            raise ServerConfigNotFoundError(f"Server '{server_name}' not found")
        return StdioServerParameters(
            command=server_params.command,
            args=server_params.args,
            env=server_params.env,
        )
    
    def update_server_path(self, server_name: str, server_path: str) -> None:
        if server_name not in self._servers_params:
            raise ServerConfigNotFoundError(f"Server '{server_name}' not found")
        self._servers_params[server_name].cwd = server_path
