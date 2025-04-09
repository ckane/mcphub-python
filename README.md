# MCP Hub

## Introduction

Welcome to the MCP Hub project! This project is focused on building a centralized hub for managing Model Context Protocol (MCP) servers, which are essential for developing AI clients that utilize MCP as tools. The MCP Hub provides a standardized way to interact with various MCP servers, making it easier for AI applications to leverage these tools effectively.

## Project Structure

The MCP Hub is designed to accommodate multiple MCP servers, each residing in the `servers/` directory. These servers are prepared to handle specific tasks and provide a wide range of functionalities that AI clients can utilize.

## Key Features

- **Server Management**: The MCP Hub initializes and manages the dependencies of each MCP server. This ensures that all necessary components are in place for the servers to function correctly.

- **Data Storage**: Information about the servers and their available tools is stored in MongoDB collections named `mcp_servers` and `mcp_tools`. This data includes:
  - **mcp_servers**: Contains details such as the command, arguments, and environment variables required to run each MCP server. This allows clients to fetch and execute servers directly.
  - **mcp_tools**: Stores information about the tools provided by each server, enabling clients to understand and utilize the available functionalities.

## Getting Started

### Prerequisites

- **MongoDB**: Ensure you have MongoDB installed and running. You can download and install MongoDB from [here](https://www.mongodb.com/try/download/community).

- **Poetry**: This project uses Poetry for dependency management. Install Poetry by following the instructions [here](https://python-poetry.org/docs/#installation).

### Setup

1. **Clone the Repository**: Clone this repository to your local machine.

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

Here's an example FastAPI application setup:

```python
from fastapi import FastAPI
from mcp_hub import setup_all_servers, store_mcp

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Setup all MCP servers
    await setup_all_servers()
    
    # Store MCP server and tool data in MongoDB
    await store_mcp()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the MCP Hub API"}

# Define additional API endpoints as needed
```

## Contributing

Contributions are welcome! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.