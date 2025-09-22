# FastMCP File Creator

A Model Context Protocol (MCP) server that provides file creation and management tools using FastMCP.

## Features

- **File Creation**: Create text files with custom content
- **Directory Listing**: List files and directories with size information
- **Interactive Client**: Command-line interface for testing server functionality

## Components

### MCP Server (`mcp_server.py`)
FastMCP-based server providing two main tools:
- `create_file`: Create text files with specified content
- `list_files`: List directory contents with file sizes

### MCP Client (`mcp_client.py`)
Interactive client for testing the MCP server functionality with async communication.

## Requirements

- Python 3.7+
- FastMCP
- MCP libraries
- python-dotenv

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your Google API key:
```
GOOGLE_API_KEY=your_api_key_here
```

## Usage

### Running the Server
```bash
python mcp_server.py
```

### Running the Interactive Client
```bash
python mcp_client.py
```

The client provides an interactive interface where you can:
- Type commands to create files or list directories
- Use 'quit' or 'exit' to terminate the session

## Tools Available

### create_file
- **Parameters**: `file_path` (string), `content` (string, optional)
- **Description**: Creates a text file at the specified path with given content
- **Features**: Automatic directory creation, file verification

### list_files
- **Parameters**: `directory` (string, optional, defaults to current directory)
- **Description**: Lists all files and directories in the specified path
- **Output**: Organized display with file sizes and directory indicators

## Error Handling

- Comprehensive error handling for file operations
- Directory creation for non-existent paths
- Validation of file creation success
- Clear error messages with emoji indicators

## License

This project is for educational and development purposes.