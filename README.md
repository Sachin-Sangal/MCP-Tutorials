# MCP Weather Server
This repository contains an MCP server that exposes a weather tool using the OpenWeatherMap API and a Python client to interact with it.


## Features

- **Weather Tool**: Get current weather and temperature for any city.
- **Multiple Transports**: Supports `stdio`, `sse`, and `streamable-http` protocols.
- **SSE Client**: Python client for interacting with the server.

**Weather Service Architecture**

<img width="877" height="111" alt="image" src="https://github.com/user-attachments/assets/9839bf50-0675-4d15-b7c4-6803051d041f" />


The MCP server acts as a bridge between AI models and external APIs, providing structured access to weather data.

### Server Setup
```python
mcp = FastMCP(
    name="Weather",
    host="0.0.0.0",  # only used for SSE transport (localhost)
    port=8050,  # only used for SSE transport (set this to any port)
    stateless_http=True,
)
```
### Define Tools
```python
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
   ```

### Multiple Transports
```python
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
```

### Building the web-client
```python
async def main():
    # Connect to the server using SSE
    async with sse_client("http://localhost:8050/sse") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()

            # List available tools
            tools_result = await session.list_tools()
            print("Available tools:")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")

            # Call the weather tool
            location = "London"
            result = await session.call_tool("get_weather", arguments={"location": location})
            print(f"Weather in {location}: {result.content[0].text}")
```
### Docker File
```python
# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN pip install uv

# Copy requirements file
COPY requirements.txt .

# Install dependencies using uv
RUN uv venv
RUN uv pip install -r requirements.txt

# Copy application code
COPY weather.py .

# Expose port
EXPOSE 8050

# Command to run the server
CMD ["uv", "run", "weather.py"]

```
### MCP Gateway

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Team Client   │    │   Team Client   │    │   Team Client   │
│     (Web App)   │    │  (Desktop App)  │    │   (CLI Tool)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │    MCP Gateway          │
                    │  - Tool Discovery       │
                    │  - Health Monitor       │
                    │  - Request Routing      │
                    │  - Protocol Translation │
                    └─────────────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Weather Server │    │   News Server   │    │ Custom Server   │
│     (Port 8001) │    │   (Port 8002)   │    │   (Port 8003)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
