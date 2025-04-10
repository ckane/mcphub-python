from dataclasses import asdict
from typing import List, Optional, Dict, Any
import os
import asyncio
from agents.mcp import MCPServerStdio
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from .mcp_server_config import MCPServerConfig, list_servers, validate_server_env  # Import from new file

load_dotenv()

# MongoDB configuration
MONGO_URI = f"mongodb://{os.getenv('MONGODB_USER')}:{os.getenv('MONGODB_PASSWORD')}@{os.getenv('MONGO_HOST')}:{os.getenv('MONGO_PORT')}"
DB_NAME = os.getenv("MONGODB_DB_NAME", "xvista_agent")

# Initialize MongoDB client
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client[DB_NAME]

async def setup_server(server_config: MCPServerConfig) -> None:
    """
    Sets up a single MCP server using its configuration.
    """
    if not os.path.exists(server_config.server_path):
        raise FileNotFoundError(f"Server directory not found: {server_config.server_path}")
    
    # Change to server directory and run setup script
    current_dir = os.getcwd()
    try:
        os.chdir(server_config.server_path)
        process = await asyncio.create_subprocess_shell(
            server_config.setup_script,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            raise Exception(f"Setup failed for {server_config.name}: {stderr.decode()}")
            
    finally:
        os.chdir(current_dir)

async def list_tools() -> Dict[str, List[Dict[str, Any]]]:
    """
    Returns a dictionary of tools from all configured MCP servers.
    The dictionary keys are server names and values are lists of tools.
    """
    servers = list_servers()
    tools_by_server = {}
    
    for server_config in servers:
        try:
            async with MCPServerStdio(
                params={
                    "command": server_config.command,
                    "args": server_config.args,
                    "cwd": server_config.server_path,
                    "env": server_config.env
                }
            ) as server:
                tools = await server.list_tools()
                tools_by_server[server_config.name] = tools
                
        except Exception as e:
            print(f"Error getting tools from {server_config.name}: {str(e)}")
            tools_by_server[server_config.name] = []
    
    return tools_by_server

async def setup_all_servers() -> None:
    """
    Sets up all configured MCP servers.
    """
    servers = list_servers()
    for server_config in servers:
        try:
            await setup_server(server_config)
            print(f"Successfully set up {server_config.name}")
        except Exception as e:
            print(f"Failed to set up {server_config.name}: {str(e)}")

async def store_mcp() -> None:
    """
    Stores MCP server configurations and their tools in MongoDB.
    Creates/updates two collections:
    - mcp_servers: Server configurations
    - mcp_tools: Tools available from each server
    """
    servers = list_servers()
    tools = await list_tools()
    
    # Get MongoDB collections
    servers_collection = db.mcp_servers
    tools_collection = db.mcp_tools
    
    # Store timestamp for this update
    timestamp = datetime.utcnow()
    
    # Store server configurations
    for server in servers:
        server_data = {
            **asdict(server),
            "updated_at": timestamp,
            "status": "active"
        }
        
        # Update or insert server configuration
        await servers_collection.update_one(
            {"name": server.name},
            {"$set": server_data},
            upsert=True
        )
    
    # Store tools data
    for server_name, server_tools in tools.items():
        # Create tool documents with server reference
        tool_documents = []
        for tool in server_tools:
            tool_doc = {
                "server_name": server_name,
                "name": tool.name,
                "description": tool.description,
                "updated_at": timestamp
            }
            tool_documents.append(tool_doc)
        
        if tool_documents:
            # Remove old tools for this server
            await tools_collection.delete_many({"server_name": server_name})
            
            # Insert new tools
            await tools_collection.insert_many(tool_documents)
    
    # Optional: Remove servers and tools that no longer exist
    current_server_names = {server.name for server in servers}
    await servers_collection.update_many(
        {"name": {"$nin": list(current_server_names)}},
        {"$set": {"status": "inactive", "updated_at": timestamp}}
    )

async def get_stored_servers() -> List[Dict[str, Any]]:
    """
    Retrieves stored server configurations from MongoDB.
    """
    servers_collection = db.mcp_servers
    return await servers_collection.find({"status": "active"}).to_list(None)

async def get_stored_tools(server_name: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Retrieves stored tools from MongoDB.
    Args:
        server_name: Optional server name to filter tools by server
    """
    tools_collection = db.mcp_tools
    query = {"server_name": server_name} if server_name else {}
    return await tools_collection.find(query).to_list(None)
