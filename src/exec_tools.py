
import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


async def execute(tool_name:str,arguments:dict[str,object]):
    # Connect to a streamable HTTP server
    async with streamable_http_client("http://localhost:8000/mcp") as (
        read_stream,
        write_stream,
        _,
    ):
        # Create a session using the client streams
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()
            # List available tools
            tools = await session.list_tools()
            print(f"Available tools: {[tool.name for tool in tools.tools]}")

            alerts=await session.call_tool(name=tool_name,arguments=arguments)
            result=""
            for content in alerts.content:
                if content.type=="text":
                    result+=content.text
            
            return result


if __name__ == "__main__":
    print(asyncio.run(execute("get_alerts",{"state":"CA"})))