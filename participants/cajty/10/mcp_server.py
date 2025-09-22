import os
from fastmcp import FastMCP

mcp = FastMCP("File Creator Server")


@mcp.tool()
def create_file(file_path: str, content: str = "This is a sample file.") -> str:
    """
    Create a text file with the specified content.

    Args:
        file_path: Path where the file should be created
        content: Text content to write to the file (optional, defaults to sample text)

    Returns:
        Success message or error description
    """
    try:
        # Get absolute path to see where we're creating the file
        abs_path = os.path.abspath(file_path)

        # Ensure the directory exists
        directory = os.path.dirname(abs_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        # Write the file
        with open(abs_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # Verify the file was created
        if os.path.exists(abs_path):
            file_size = os.path.getsize(abs_path)
            return f"✅ Successfully created file: {abs_path} ({file_size} bytes)"
        else:
            return f"❌ File creation failed: {abs_path}"

    except Exception as e:
        return f"❌ Error creating file: {str(e)}"


@mcp.tool()
def list_files(directory: str = ".") -> str:
    """
    List files in the specified directory.

    Args:
        directory: Directory path to list (defaults to current directory)

    Returns:
        List of files and directories
    """
    try:
        # Get absolute path
        abs_directory = os.path.abspath(directory)

        if not os.path.exists(abs_directory):
            return f"❌ Directory does not exist: {abs_directory}"

        items = os.listdir(abs_directory)
        if not items:
            return f"📂 Directory {abs_directory} is empty"

        files = []
        dirs = []

        for item in items:
            item_path = os.path.join(abs_directory, item)
            if os.path.isfile(item_path):
                file_size = os.path.getsize(item_path)
                files.append(f"📄 {item} ({file_size} bytes)")
            else:
                dirs.append(f"📁 {item}/")

        result = f"Contents of {abs_directory}:\n"
        if dirs:
            result += "\n".join(sorted(dirs)) + "\n"
        if files:
            if dirs:
                result += "\n"
            result += "\n".join(sorted(files))

        return result

    except Exception as e:
        return f"❌ Error listing directory: {str(e)}"


if __name__ == "__main__":
    # Remove the Windows-specific stdin/stdout handling
    # The MCP library handles this internally
    mcp.run()