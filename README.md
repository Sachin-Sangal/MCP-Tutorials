# MCP Weather Server
This repository contains an MCP server that exposes a weather tool using the [OpenWeatherMap API](https://openweathermap.org/api), and a Python SSE client to interact with it.


## Features

- **Weather Tool**: Get current weather and temperature for any city.
- **Multiple Transports**: Supports `stdio`, `sse`, and `streamable-http` protocols.
- **SSE Client**: Example Python client for interacting with the server via SSE.

**Weather Service Architecture**

<img width="877" height="111" alt="image" src="https://github.com/user-attachments/assets/9839bf50-0675-4d15-b7c4-6803051d041f" />


The MCP server acts as a bridge between AI models and external APIs, providing structured access to weather data.

### Installation

1. Clone the repository:
    ```
    git clone https://github.com/<your-username>/<repo-name>.git
    cd <repo-name>
    ```

2. Install dependencies:
    ```
    pip install requests nest_asyncio
    ```

3. (Optional) Install MCP toolkit if not already:
    ```
    git clone https://github.com/microsoft/mcp-toolkit.git
    cd mcp-toolkit
    pip install .
    ```

### Configuration

- Edit `weather.py` and set your OpenWeatherMap API key:
    ```python
    OPENWEATHER_API_KEY = "your_api_key_here"
    ```

## Usage

### Start the MCP Weather Server

You can run the server with any supported transport:

- **SSE:**
    ```
    python weather.py sse
    ```
- **Stdio:**
    ```
    python weather.py stdio
    ```
- **Streamable HTTP:**
    ```
    python weather.py streamable_http
    ```

### Run the SSE Client

Make sure the server is running with SSE transport:

```
python client.py
```

## Example Output

```
Available tools:
  - get_weather: Get current weather for a location
Weather in London: Clear sky, 22°C
```

## License

MIT

---

**Note:**  
Replace `<your-username>/<repo-name>` with your actual GitHub username and repository name.
