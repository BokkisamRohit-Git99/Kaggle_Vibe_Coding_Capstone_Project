import sys
import os
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def fetch_background_location() -> str:
    """
    Communicates directly with the local ThinAir Geo MCP Server 
    over a secure stdio memory pipeline.
    """
    # Build absolute file path mapping to the geo_server execution file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    server_path = os.path.abspath(os.path.join(current_dir, "..", "mcp_server", "geo_server.py"))
    
    server_params = StdioServerParameters(
        command=sys.executable,  # Points to your active python environment (.venv)
        args=[server_path],
        env=os.environ.copy()
    )
    
    try:
        # Establish the sandboxed stdio runtime socket channel
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                # Initialize the handshake sequence protocol
                await session.initialize()
                
                # Execute the location tracking tool silently
                result = await session.call_tool("get_precise_location")
                
                if result and result.content:
                    location_text = result.content[0].text
                    if "Error" in location_text:
                        raise RuntimeError(location_text)
                    return location_text
                raise ValueError("Received empty packet back from MCP telemetry server.")
    except Exception as e:
        raise RuntimeError(f"MCP Telemetry Engine Failed: {str(e)}")