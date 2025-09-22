import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

FASTMCP_SERVER_SCRIPT = "mcp_server.py"


class FastMCPClient:
    """Simplified MCP client"""

    def __init__(self):
        self.session = None
        self.available_tools = []

    async def connect(self):
        """Connect to the FastMCP server"""
        print("🔗 Connecting to FastMCP server...")
        server_params = StdioServerParameters(command="python", args=[FASTMCP_SERVER_SCRIPT])

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                self.session = session
                await session.initialize()
                tools_result = await session.list_tools()
                self.available_tools = tools_result.tools
                print(f"✅ Connected! Available tools: {[tool.name for tool in self.available_tools]}")

    async def call_tool(self, tool_name: str, arguments: dict) -> str:
        """Call an MCP tool"""
        try:
            print(f"🔧 Calling tool: {tool_name}({arguments})")
            result = await self.session.call_tool(tool_name, arguments)
            return result.content[0].text if result.content and result.content[0].text else "✅ Tool executed successfully"
        except Exception as e:
            return f"❌ Tool error: {str(e)}"

    async def run_interactive(self):
        """Run interactive mode"""
        print("\n🤖 FastMCP File Creator")
        print("Type 'quit' to exit.")

        async with stdio_client(StdioServerParameters(command="python", args=[FASTMCP_SERVER_SCRIPT])) as (read, write):
            async with ClientSession(read, write) as session:
                self.session = session
                await session.initialize()
                tools_result = await session.list_tools()
                self.available_tools = tools_result.tools
                print(f"✅ Connected! Available tools: {[tool.name for tool in self.available_tools]}")

                while True:
                    user_input = input("\n💬 You: ").strip()
                    if user_input.lower() in ['quit', 'exit']:
                        print("👋 Goodbye!")
                        break
                    if not user_input:
                        continue
                    print("🤖 Processing...")
                    tool_name = "list_files" if "list" in user_input else "create_file"
                    arguments = {"directory": "."} if tool_name == "list_files" else {"file_path": "example.txt", "content": "Sample content"}
                    response = await self.call_tool(tool_name, arguments)
                    print(f"🤖 Response: {response}")


def main():
    """Main function"""
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY not found in .env file")
        return

    print("🤖 FastMCP File Creator")
    try:
        client = FastMCPClient()
        asyncio.run(client.run_interactive())
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()