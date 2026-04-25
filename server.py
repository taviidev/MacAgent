import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types

from tools.llm import call_llama
from tools.shell import run_shell
from tools.files import read_file, list_dir, write_file, grep_search
from tools.browser import fetch_url

# Create the server instance
server = Server("mac-code-mcp")

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="chat",
            description="Send a prompt to the local LLM",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {"type": "string"}
                },
                "required": ["prompt"]
            }
        ),
        types.Tool(
            name="shell",
            description="Execute a shell command",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {"type": "string"}
                },
                "required": ["command"]
            }
        ),
        types.Tool(
            name="read_file",
            description="Read the content of a file from the local file system",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Absolute path to the file"}
                },
                "required": ["path"]
            }
        ),
        types.Tool(
            name="list_dir",
            description="List the contents of a directory from the local file system",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Absolute path to the directory"}
                },
                "required": ["path"]
            }
        ),
        types.Tool(
            name="write_file",
            description="Write content to a file on the local file system",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Absolute path to the file"},
                    "content": {"type": "string", "description": "The content to write to the file"}
                },
                "required": ["path", "content"]
            }
        ),
        types.Tool(
            name="grep_search",
            description="Search for a pattern in a directory using grep",
            inputSchema={
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "The pattern to search for"},
                    "path": {"type": "string", "description": "Absolute path to the directory to search in"}
                },
                "required": ["pattern", "path"]
            }
        ),
        types.Tool(
            name="fetch_url",
            description="Download a URL and extract its text content to read documentation or news",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "The URL to fetch content from"}
                },
                "required": ["url"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Handle tool calls."""
    if name == "chat":
        prompt = arguments.get("prompt", "")
        result = call_llama(prompt)
        return [types.TextContent(type="text", text=str(result))]

    elif name == "shell":
        command = arguments.get("command", "")
        result = run_shell(command)
        return [types.TextContent(type="text", text=str(result))]

    elif name == "read_file":
        path = arguments.get("path", "")
        result = read_file(path)
        return [types.TextContent(type="text", text=str(result))]

    elif name == "list_dir":
        path = arguments.get("path", "")
        result = list_dir(path)
        return [types.TextContent(type="text", text=str(result))]

    elif name == "write_file":
        path = arguments.get("path", "")
        content = arguments.get("content", "")
        result = write_file(path, content)
        return [types.TextContent(type="text", text=str(result))]

    elif name == "grep_search":
        pattern = arguments.get("pattern", "")
        path = arguments.get("path", "")
        result = grep_search(pattern, path)
        return [types.TextContent(type="text", text=str(result))]

    elif name == "fetch_url":
        url = arguments.get("url", "")
        result = fetch_url(url)
        return [types.TextContent(type="text", text=str(result))]

    else:
        return [types.TextContent(type="text", text=f"Unknown tool: {name}")]

async def main():
    """Run the server using stdin/stdout streams."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
