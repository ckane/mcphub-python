# MCPHub

A hub for Model Context Protocol (MCP) servers that enables you to manage and run MCP servers locally.

## Installation

```bash
pip install mcphub
```

## Usage

### Command Line Interface

MCPHub comes with a command-line interface for common operations:

```bash
# Set up all configured MCP servers
mcphub setup

# List available MCP servers
mcphub list-servers

# List tools from all MCP servers
mcphub list-tools

# List tools from a specific server
mcphub list-tools --server azure-devops

# Use the MCPHubAdapter
mcphub adapter --config mcp_config.json --server azure-devops-mcp
```

### Using in code

```python
import asyncio
from mcphub import MCPHubAdapter, setup_all_servers, store_mcp, list_tools
from dataclasses import asdict

# Initialize and set up servers
async def init():
    await setup_all_servers()
    await store_mcp()
    
    # List all available tools
    tools = await list_tools()
    print(f"Available tools: {tools}")
    
    # Use the adapter to get a specific server
    adapter = MCPHubAdapter().from_config("mcp_config.json", cache_path="cache")
    server = adapter.get_server("azure-devops-mcp")
    
    if server:
        print(f"Server config: {server}")

# Run the async function
asyncio.run(init())
```