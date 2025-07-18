# mcp-pyats
This is a work in progress MCP server that uses pyATS to interact with network devices.  In its initial form, it only sends "show commands" and returns the results. But I'm working on adding additional "tools" to the framework. 

This MCP server is built using [FastMCP 2.0](https://gofastmcp.com/getting-started/welcome).  Clients connect to it using HTTP, and the server is written to run on port 8002.  

```
# Example
python main.py                 

╭─ FastMCP 2.0 ──────────────────────────────────────────────────────────────╮
│                                                                            │
│        _ __ ___ ______           __  __  _____________    ____    ____     │
│       _ __ ___ / ____/___ ______/ /_/  |/  / ____/ __ \  |___ \  / __ \    │
│      _ __ ___ / /_  / __ `/ ___/ __/ /|_/ / /   / /_/ /  ___/ / / / / /    │
│     _ __ ___ / __/ / /_/ (__  ) /_/ /  / / /___/ ____/  /  __/_/ /_/ /     │
│    _ __ ___ /_/    \__,_/____/\__/_/  /_/\____/_/      /_____(_)____/      │
│                                                                            │
│                                                                            │
│                                                                            │
│    🖥️  Server name:     FastMCP                                             │
│    📦 Transport:       Streamable-HTTP                                     │
│    🔗 Server URL:      http://127.0.0.1:8002/mcp/                          │
│                                                                            │
│    📚 Docs:            https://gofastmcp.com                               │
│    🚀 Deploy:          https://fastmcp.cloud                               │
│                                                                            │
│    🏎️  FastMCP version: 2.10.5                                              │
│    🤝 MCP version:     1.11.0                                              │
│                                                                            │
╰────────────────────────────────────────────────────────────────────────────╯


[07/18/25 12:06:16] INFO     Starting MCP server 'FastMCP' with transport 'http' on http://127.0.0.1:8002/mcp/                                     server.py:1448
INFO:     Started server process [87511]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8002 (Press CTRL+C to quit)
```

Clients, such as LMStudio, can be configured to connect to the server with this configuration: 

```json
{
  "mcpServers": {
    "pyats": {
      "url": "http://localhost:8002/mcp"
    }
  }
}
```

Be sure to use an LLM that supports tool use.  This server has been tested with: 

* [google/gemma-2-9b](https://lmstudio.ai/models/google/gemma-2-9b)
* [qwen/qwen3-4b](https://lmstudio.ai/models/qwen/qwen3-4b)
