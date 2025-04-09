from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# MongoDB configuration
MONGO_URI = f"mongodb://{os.getenv('MONGODB_USER')}:{os.getenv('MONGODB_PASSWORD')}@{os.getenv('MONGO_HOST')}:{os.getenv('MONGO_PORT')}"
DB_NAME = os.getenv("MONGODB_DB_NAME", "xvista_agent")

# Initialize MongoDB client
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client[DB_NAME]

async def list_servers() -> List[Dict[str, Any]]:
    """
    Lists all MCP servers from the database.
    """
    servers_collection = db.mcp_servers
    return await servers_collection.find({"status": "active"}).to_list(None)

async def get_server(server_name: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves a specific MCP server by name.
    """
    servers_collection = db.mcp_servers
    return await servers_collection.find_one({"name": server_name, "status": "active"})

async def list_tools(server_name: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Lists all tools, optionally filtered by server name.
    """
    tools_collection = db.mcp_tools
    query = {"server_name": server_name} if server_name else {}
    return await tools_collection.find(query).to_list(None)

async def get_tool(server_name: str, tool_name: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves a specific tool by server name and tool name.
    """
    tools_collection = db.mcp_tools
    return await tools_collection.find_one({"server_name": server_name, "name": tool_name})

async def insert_user_agent_mcp(user_id: str, agent_id: str, mcp_data: Dict[str, Any]) -> None:
    """
    Inserts a new MCP entry for a user-agent.
    """
    user_agents_collection = db.user_agents
    await user_agents_collection.insert_one({
        "user_id": ObjectId(user_id),
        "agent_id": ObjectId(agent_id),
        "mcp_data": mcp_data,
        "created_at": datetime.now(datetime.UTC)
    })

async def list_user_agent_mcp(user_id: str, agent_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Lists all MCPs for a given user-agent.
    """
    user_agents_collection = db.user_agents
    query = {"user_id": user_id}
    if agent_id:
        query["agent_id"] = agent_id
    return await user_agents_collection.find(query).to_list(None) 