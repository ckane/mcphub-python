from typing import Dict, List, Any, Optional
from pathlib import Path
import json
import yaml
import os
import subprocess
from pathlib import Path

# from mcp_hub import setup_all_servers, store_mcp, list_tools as hub_list_tools
from mcp_server_config import MCPServerConfig, list_servers, validate_server_env
# from mcp_controller import get_server, get_tool, list_servers as list_db_servers
from .base import BaseAdapter

class MCPHubAdapter(BaseAdapter):
    """Adapter for loading tools from MCP Hub."""
    
    def __init__(self):
        self.cache_path = None
        self.servers = []

    def from_config(self, config_path: str, cache_path: str = None) -> 'MCPHubAdapter':
        # Create cache directory if it doesn't exist
        if cache_path:
            self.cache_path = Path(cache_path)
            os.makedirs(self.cache_path, exist_ok=True)
        
        # Load the configuration
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            
        # Process each server in the config
        for server_type, servers in config.items():
            for server in servers:
                repo_name = server.get('name')
                if repo_name:
                    # Clone repository if cache path is provided
                    if self.cache_path:
                        repo_dir = self.cache_path / repo_name.split('/')[-1]
                        if not repo_dir.exists():
                            print(f"Cloning {repo_name} into {repo_dir}")
                            subprocess.run(
                                ["git", "clone", f"https://github.com/{repo_name}.git", str(repo_dir)],
                                check=True
                            )
                        else:
                            print(f"Repository {repo_name} already exists at {repo_dir}")
                    
                    # Store server information
                    self.servers.append({
                        'type': server_type,
                        'name': repo_name,
                        'env': server.get('env', {})
                    })
        
        return self
    
    @property
    def get_server(self) -> List[MCPServerConfig]:
        pass