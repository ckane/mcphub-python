from dataclasses import dataclass
from typing import List, Dict
import os
from pathlib import Path

@dataclass
class MCPServerConfig:
    name: str
    command: str
    args: List[str]
    env: Dict[str, str]
    setup_script: str
    server_path: str

def list_servers() -> List[MCPServerConfig]:
    """
    Returns a list of MCP server configurations.
    Each configuration includes the server parameters and setup instructions.
    """
    # Base directory for all MCP servers
    base_dir = Path(__file__).parent / "servers"
    
    servers = [
        MCPServerConfig(
            name="azure-devops",
            command="node",
            args=["dist/index.js"],
            env={
                "AZURE_DEVOPS_ORG_URL": os.getenv("AZURE_DEVOPS_ORG_URL", "NOT SET"),
                "AZURE_DEVOPS_AUTH_METHOD": os.getenv("AZURE_DEVOPS_AUTH_METHOD", "azure-identity"),
                "AZURE_DEVOPS_DEFAULT_PROJECT": os.getenv("AZURE_DEVOPS_DEFAULT_PROJECT", "NOT SET"),
                "AZURE_DEVOPS_PAT": os.getenv("AZURE_DEVOPS_PAT", "NOT SET"),
            },
            setup_script="npm install && npm run build",
            server_path=str(base_dir / "mcp-server-azure-devops")
        ),
        # Add more servers here as you clone them
        # Example:
        # MCPServerConfig(
        #     name="another-server",
        #     command="npx",
        #     args=[...],
        #     env={...},
        #     setup_script="npm install && npm run build",
        #     server_path=str(base_dir / "another-server")
        # ),
    ]
    
    return servers 