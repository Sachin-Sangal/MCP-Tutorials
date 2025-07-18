import sys
import json
import requests

import mcp
from mcp.server.fastmcp import FastMCP

OPENWEATHER_API_KEY = ""  # Replace with your actual API key

mcp = FastMCP(
    name="Weather",
    host="0.0.0.0",  # only used for SSE transport (localhost)
    port=8050,  # only used for SSE transport (set this to any port)
    stateless_http=True,
)

@mcp.tool()
def get_weather(location: str = "London") -> dict:
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            "location": location,
            "weather": data["weather"][0]["description"],
            "temperature": data["main"]["temp"]
        }
    else:
        return {"error": f"API error: {response.status_code}"}



if __name__ == "__main__":
    transport = "sse"
    if transport == "stdio":
        print("Running server with stdio transport")
        mcp.run(transport="stdio")
    elif transport == "sse":
        print("Running server with SSE transport")
        mcp.run(transport="sse")
    elif transport == "streamable-http":
        print("Running server with Streamable HTTP transport")
        mcp.run(transport="streamable-http")
    else:
        raise ValueError(f"Unknown transport: {transport}")