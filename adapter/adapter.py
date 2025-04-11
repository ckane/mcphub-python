from typing import Dict, List, Optional
from pathlib import Path
import json
import yaml
import os
from pathlib import Path
from .base import BaseAdapter
from dataclasses import dataclass

@dataclass
class MCPServerConfig:
    name: str
    command: str
    args: List[str]
    env: Dict[str, str]
    description: Optional[str] = None
    tags: Optional[List[str]] = None

class MCPHubAdapter(BaseAdapter):
    """Adapter for loading tools from MCP Hub."""
    
    def __init__(self):
        self.cache_path = None
        self.servers: List[MCPServerConfig] = []

    def from_config(self, config_path: str, cache_path: str = None) -> 'MCPHubAdapter':
        # Create cache directory if it doesn't exist
        if cache_path:
            self.cache_path = Path(cache_path)
            os.makedirs(self.cache_path, exist_ok=True)
        
        # Load the configuration
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Load server commands if available
        commands_path = Path(__file__).parent / "mcp_server_commands.json"
        if commands_path.exists():
            with open(commands_path, 'r') as f:
                server_commands = json.load(f)
        else:
            server_commands = {}
            
        # Process each server in the config
        for server_type, servers in config.items():
            for server in servers:
                repo_name = server.get('name')
                if repo_name:
                    if repo_name not in server_commands:
                        raise ValueError(
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
                    
                    self.servers.append(MCPServerConfig(**server_info))
        
        return self
    
    @property
    def get_servers(self) -> List[MCPServerConfig]:
        """Return the list of server configurations."""
        return self.servers