from adapter.adapter import MCPHubAdapter

# Or use the cache path from the config file
adapter = MCPHubAdapter().from_config(config_path="mcp_config.yaml", cache_path="./cache")
# tools = adapter.load_tools()

# print(tools)