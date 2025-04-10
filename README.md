# MCP Hub

## Introduction

Welcome to the MCP Hub project! This project enables you to deploy and manage your own **Model Context Protocol (MCP) servers locally**. Rather than relying on external MCP services, MCP Hub lets you run MCP servers directly on your infrastructure, giving you full control over your AI tools. The MCP Hub provides a standardized way to deploy, configure and interact with various local MCP servers, making it easier for AI applications to leverage these tools effectively while maintaining data privacy and reducing external dependencies.

## Project Structure

The MCP Hub is designed to accommodate multiple MCP servers, each residing in the `servers/` directory. These servers are prepared to handle specific tasks and provide a wide range of functionalities that AI clients can utilize.

## Key Features

- **Server Management**: The MCP Hub initializes and manages the dependencies of each MCP server. This ensures that all necessary components are in place for the servers to function correctly.

- **Data Storage**: Information about the servers and their available tools is stored in MongoDB collections named `mcp_servers` and `mcp_tools`. This data includes:
  - **mcp_servers**: Contains details such as the command, arguments, and environment variables required to run each MCP server. This allows clients to fetch and execute servers directly.
  - **mcp_tools**: Stores information about the tools provided by each server, enabling clients to understand and utilize the available functionalities.

## Database Structure

The MCP Hub uses MongoDB to store information about the servers and tools. Here is an overview of the database structure:

### `mcp_servers` Collection

This collection stores the configuration details for each MCP server. Each document in the collection includes:

- **name**: The name of the MCP server.
- **command**: The command used to start the server.
- **args**: A list of arguments for the command.
- **env**: A dictionary of environment variables required by the server.
- **setup_script**: The script used to set up the server.
- **server_path**: The file path to the server's directory.
- **updated_at**: A timestamp indicating when the server configuration was last updated.
- **status**: The current status of the server (e.g., "active" or "inactive").

### `mcp_tools` Collection

This collection stores information about the tools available from each MCP server. Each document in the collection includes:

- **server_name**: The name of the server providing the tool.
- **name**: The name of the tool.
- **description**: A brief description of what the tool does.
- **updated_at**: A timestamp indicating when the tool information was last updated.

## Getting Started

### Prerequisites

- **MongoDB**: Ensure you have MongoDB installed and running. You can download and install MongoDB from [here](https://www.mongodb.com/try/download/community).

- **Poetry**: This project uses Poetry for dependency management. Install Poetry by following the instructions [here](https://python-poetry.org/docs/#installation).

- **uv**: This project uses uv for faster Python package installation. Install uv by following the instructions [here](https://github.com/astral-sh/uv#installation).

- **npm**: Some MCP servers require Node.js and npm. Install Node.js and npm by following the instructions [here](https://nodejs.org/en/download/).

### Setup

1. **Clone the Repository**: Clone this repository into the `vista_mcp_hub` directory from the root of your project:

   ```bash
   git clone --recurse-submodules https://dev.azure.com/azurefsoft062/agent-vista-platform/_git/vista-mcp-hub vista_mcp_hub
   cd vista_mcp_hub
   ```

2. **Install Dependencies**: Navigate to the project directory and run the following command to install the necessary Python packages using Poetry:

   ```bash
   poetry install
   ```

3. **Configure Environment Variables**: Copy the `.env.tmp` file to `.env` and fill in the required values, such as MongoDB credentials and Azure DevOps settings. Here is an example of what your `.env` file might look like:

   ```plaintext
   MONGODB_USER=your_username
   MONGODB_PASSWORD=your_password
   MONGO_HOST=localhost
   MONGO_PORT=27017
   MONGODB_DB_NAME=xvista_agent

   AZURE_DEVOPS_ORG_URL=https://dev.azure.com/your-organization
   AZURE_DEVOPS_AUTH_METHOD=azure-identity
   AZURE_DEVOPS_DEFAULT_PROJECT=your-project-name
   AZURE_DEVOPS_PAT=your_personal_access_token

   LOG_LEVEL=info
   ```

4. **Run the MCP Hub**: Execute the main script to initialize the servers and store their configurations and tools in MongoDB.

### Using MCP Hub in FastAPI

To integrate the MCP Hub with a FastAPI application, follow these steps:

1. **Import MCP Hub Functions**: Import the necessary functions from `mcp_hub.py` in your FastAPI application.

2. **Setup MCP Servers on Startup**: Use FastAPI's startup event to initialize MCP servers and store their configurations.

3. **Validate Environment Variables**: Before using a server, ensure that all required environment variables are set. Use the `validate_server_env` function to check for any unset variables. This function will raise an `EnvironmentError` if any required environment variable is not set.

Here's an example FastAPI application setup:

```python
from fastapi import FastAPI
from vista_mcp_hub.mcp_hub import setup_all_servers, store_mcp, setup_server, list_tools
from vista_mcp_hub.mcp_server_config import list_servers, validate_server_env

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Setup all MCP servers
    await setup_all_servers()
    
    # Store MCP server and tool data in MongoDB
    await store_mcp()

@app.get("/use-server/{server_name}")
async def use_server(server_name: str):
    servers = list_servers()
    server_config = next((s for s in servers if s.name == server_name), None)
    
    if not server_config:
        return {"error": f"Server '{server_name}' not found."}
    
    # Validate environment variables before using the server
    try:
        validate_server_env(server_config)
    except EnvironmentError as e:
        return {"error": str(e)}
    
    # Proceed with using the server
    # Example: setup the server or list tools
    await setup_server(server_config)
    tools = await list_tools()
    return {"tools": tools[server_name]}

@app.get("/")
async def read_root():
    return {"message": "Welcome to the MCP Hub API"}

# Define additional API endpoints as needed
```

## Contributing

Contributions are welcome! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.