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


