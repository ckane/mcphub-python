from typing import Dict, List, Optional, Union
from pathlib import Path
import json
import yaml
import os
from .base import BaseAdapter
from dataclasses import dataclass

class MCPHubAdapterError(Exception):
    """Base exception for MCPHubAdapter errors."""
    pass

class ServerConfigNotFoundError(MCPHubAdapterError):
    """Raised when a server configuration is not found."""
    pass

@dataclass
class MCPServerConfig:
    """Configuration for an MCP server.
    
    Attributes:
        name: The server name
        command: Command to start the server
        args: Command line arguments for the server
        env: Environment variables for the server
        description: Optional description of the server
        tags: Optional tags for categorizing the server
    """
    name: str
    command: str
    args: List[str]
    env: Dict[str, str]
    description: Optional[str] = None
    tags: Optional[List[str]] = None

class MCPHubAdapter(BaseAdapter):
    """Adapter for loading tools from MCP Hub.
    
    This adapter handles loading and managing MCP server configurations.
    """
    
    def __init__(self):
        """Initialize the MCPHubAdapter."""
        self._cache_path = None
        self._servers: Dict[str, MCPServerConfig] = {}

    @classmethod
    def from_config(cls, config_path: str, cache_path: Optional[str] = None) -> 'MCPHubAdapter':
        """Create an adapter instance from a configuration file.
        
        Args:
            config_path: Path to the configuration YAML file
            cache_path: Optional path to store cache data
            
        Returns:
            MCPHubAdapter: Configured adapter instance
            
        Raises:
            ServerConfigNotFoundError: If a server is not found in commands list
            FileNotFoundError: If the config file cannot be found
            yaml.YAMLError: If the config file has invalid YAML
        """
        instance = cls()
        
        # Create cache directory if it doesn't exist
        if cache_path:
            instance._cache_path = Path(cache_path)
            os.makedirs(instance._cache_path, exist_ok=True)
        
        # Load the configuration
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Invalid YAML in configuration file: {e}")
        
        # Load server commands if available
        commands_path = Path(__file__).parent / "mcp_server_commands.json"
        server_commands = {}
        if commands_path.exists():
            with open(commands_path, 'r') as f:
                server_commands = json.load(f)
            
        # Process each server in the config
        for server_type, servers in config.items():
            for server in servers:
                repo_name = server.get('name')
                if repo_name:
                    if repo_name not in server_commands:
                        raise ServerConfigNotFoundError(
                            f"Server '{repo_name}' not found in mcp_server_commands.json. "
                            f"Please add command and args configuration for this server."
                        )
                    
                    # Get command details from the commands file
                    cmd_info = server_commands[repo_name]
                    
                    # Store server information with command details from commands file
                    server_info = {
                        'name': repo_name,
                        'env': server.get('env', {}),
                        'command': cmd_info.get('command'),
                        'args': cmd_info.get('args'),
                        'description': cmd_info.get('description'),
                        'tags': cmd_info.get('tags')
                    }
                    
                    instance._servers[server_type] = MCPServerConfig(
                        name=server_info['name'],
                        command=server_info['command'],
                        args=server_info['args'],
                        env=server_info['env'],
                        description=server_info.get('description'),
                        tags=server_info.get('tags')
                    )
                else:
                    raise ServerConfigNotFoundError(
                        "Server configuration missing 'name' field."
                    )
        
        return instance
    
    @property
    def servers(self) -> Dict[str, MCPServerConfig]:
        """Get the server configurations.
        
        Returns:
            Dictionary of server configurations
        """
        return self._servers
    
    @property
    def cache_path(self) -> Optional[Path]:
        """Get the cache directory path.
        
        Returns:
            Path to the cache directory or None if not set
        """
        return self._cache_path
    
    def get_server(self, server_type: str) -> Union[MCPServerConfig, None]:
        """Get a specific server configuration.
        
        Args:
            server_type: Type of the server to retrieve
            
        Returns:
            MCPServerConfig: The requested server configuration or None if not found
        """
        return self._servers.get(server_type)