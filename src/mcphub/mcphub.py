from typing import Dict, List, Optional
from pathlib import Path
import json
import yaml
from dataclasses import dataclass, field

# Define the custom exception
class ServerConfigNotFoundError(Exception):
    """Raised when a server configuration is not found."""
    pass

@dataclass
class MCPServerConfig:
    name: str
    command: str
    args: List[str]
    env: Dict[str, str]
    description: Optional[str] = None
    tags: Optional[List[str]] = None

@dataclass
class MCPHub:
    servers: Dict[str, MCPServerConfig] = field(default_factory=dict)

    def __post_init__(self):
        config_path = self._find_config_path()
        self.servers = self._load_and_process_config(config_path)

    def _find_config_path(self) -> str:
        current_dir = Path.cwd()
        for parent in [current_dir] + list(current_dir.parents):
            config_path = parent / ".mcphub.yaml"
            if config_path.exists():
                return str(config_path)
        raise FileNotFoundError("Configuration file '.mcphub.yaml' not found in the project root or any parent directories.")

    def _load_and_process_config(self, config_path: str) -> Dict[str, MCPServerConfig]:
        config = self._load_yaml_config(config_path)
        server_commands = self._load_server_commands()
        return self._process_servers(config, server_commands)

    @staticmethod
    def _load_yaml_config(config_path: str) -> Dict:
        try:
            with open(config_path, "r") as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Invalid YAML in configuration file: {e}")

    @staticmethod
    def _load_server_commands() -> Dict:
        commands_path = Path(__file__).parent / "mcphub_preconfigured_servers.json"
        print(f"Commands path: {commands_path}")
        if commands_path.exists():
            with open(commands_path, "r") as f:
                return json.load(f)
        return {}

    @staticmethod
    def _process_servers(config: Dict, server_commands: Dict) -> Dict[str, MCPServerConfig]:
        servers = {}
        for mcp_name, configs in config.items():
            if len(configs) != 1:
                raise ValueError(f"Each mcp_name must have exactly one configuration. Found {len(configs)} for '{mcp_name}'.")
            server = configs[0]
            repo_name = server.get("name")
            print(f"Processing server: {repo_name}")
            print(f"Server commands: {server_commands}")
            if repo_name and server_commands.get(repo_name):
                cmd_info = server_commands[repo_name]
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

    def get_server(self, mcp_name: str) -> Optional[MCPServerConfig]:
        return self.servers.get(mcp_name)