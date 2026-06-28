import httpx
from mcp.server.fastmcp import FastMCP

# Initialize the FastMCP Server Namespace
mcp = FastMCP("ThinAir-Geo-Server")

@mcp.tool()
async def get_precise_location() -> str:
    """
    Autonomously extracts external network metadata to pinpoint the 
    current active City, Region, and Country without user intervention.
    """
    try:
        async with httpx.AsyncClient() as client:
            # 1. Fetch public network IP address
            ip_resp = await client.get("https://api.ipify.org?format=json", timeout=3.0)
            user_ip = ip_resp.json().get("ip")
            
            if not user_ip:
                return "Error: Could not extract external network IP."

            # 2. Extract detailed localized geo-spatial data
            geo_resp = await client.get(f"https://ipapi.co/{user_ip}/json/", timeout=3.0)
            data = geo_resp.json()
            
            city = data.get('city')
            region = data.get('region')
            country = data.get('country_name')
            
            if city and region and country:
                return f"{city}, {region}, {country}"
            return "Error: Localized telemetry packets returned incomplete."
    except Exception as e:
        return f"Telemetry Processing Error: {str(e)}"

if __name__ == "__main__":
    # Run the server via standard stdio transport channel
    mcp.run(transport="stdio")