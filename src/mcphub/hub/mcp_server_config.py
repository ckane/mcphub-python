from dataclasses import dataclass
from typing import List, Dict
import os
from pathlib import Path


@dataclass
class MCPServerConfig:
    name: str
    description: str
    tags: List[str]
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
            description="Azure DevOps MCP Server",
            tags=["azure-devops", "azure"],
            command="node",
            args=["dist/index.js"],
            env={
                "AZURE_DEVOPS_ORG_URL": os.getenv("AZURE_DEVOPS_ORG_URL", "NOT SET"),
                "AZURE_DEVOPS_AUTH_METHOD": os.getenv(
                    "AZURE_DEVOPS_AUTH_METHOD", "azure-identity"
                ),
                "AZURE_DEVOPS_DEFAULT_PROJECT": os.getenv(
                    "AZURE_DEVOPS_DEFAULT_PROJECT", "NOT SET"
                ),
                "AZURE_DEVOPS_PAT": os.getenv("AZURE_DEVOPS_PAT", "NOT SET"),
            },
            setup_script="npm install && npm run build",
            server_path=str(base_dir / "mcp-server-azure-devops"),
        ),
        MCPServerConfig(
            name="azure-storage",
            description="Azure Storage MCP Server",
            tags=["azure-storage", "azure"],
            command="uv",
            args=["run", "mcp_server_azure_cmd"],
            env={},
            setup_script="uv pip install -e .",
            server_path=str(base_dir / "azure_mcp_server"),
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


def validate_server_env(server_config: MCPServerConfig) -> None:
    """
    Validates the environment variables for a given server configuration.
    Raises an exception if any environment variable is not set.
    """
    unset_vars = [key for key, value in server_config.env.items() if value == "NOT SET"]
    if unset_vars:
        raise EnvironmentError(
            f"The following environment variables are not set for server '{server_config.name}': {', '.join(unset_vars)}"
        )
