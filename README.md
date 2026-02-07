# Sessionize MCP Server

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that exposes Sessionize session data as a tool. It allows AI agents and LLM clients to search for speakers and talks by date.

## Tools

| Tool | Description |
|---|---|
| `search_sessionize` | Search for sessions by month in `Month Year` format (e.g. `April 2025`) |

## Configuration

The server is configured via environment variables:

| Variable | Description | Required |
|---|---|---|
| `SESSIONIZE_URL` | Sessionize API endpoint URL | Yes |
| `SESSIONIZE_DATE_FILTER_CATEGORY_ID` | Category ID used to filter sessions by date | Yes |

## Running Locally

### With Python

```bash
pip install -r requirements.txt

SESSIONIZE_URL="https://sessionize.com/api/v2/<your-id>/view/Sessions" \
SESSIONIZE_DATE_FILTER_CATEGORY_ID=61493 \
python src/sessionize_tool.py
```

### With Podman / Docker

```bash
podman build -t sessionize-mcp .

podman run -p 8000:8000 \
  -e SESSIONIZE_URL="https://sessionize.com/api/v2/<your-id>/view/Sessions" \
  -e SESSIONIZE_DATE_FILTER_CATEGORY_ID=61493 \
  sessionize-mcp
```

The MCP endpoint will be available at `http://localhost:8000/mcp`.

## Client Configuration

### VS Code / GitHub Copilot

Add to your `.vscode/mcp.json`:

```json
{
  "servers": {
    "sessionize": {
      "type": "http",
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "sessionize": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

### Cursor

Add to your Cursor MCP settings:

```json
{
  "mcpServers": {
    "sessionize": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

### Open WebUI

1. Go to **Settings → Tools → Add MCP Server**
2. Set the URL to `http://<host>:8000/mcp`

### curl

```bash
# Initialize session
curl -i -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"curl","version":"1.0"}}}'

# Call the tool (use mcp-session-id from the response headers above)
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: <session-id>" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"search_sessionize","arguments":{"date":"April 2025"}}}'
```
