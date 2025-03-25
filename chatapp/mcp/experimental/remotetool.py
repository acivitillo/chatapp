from mcp.server.sse import SseServerTransport
from fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse
from starlette.routing import Mount
from starlette.requests import Request

# Initialize FastMCP server
mcp = FastMCP("sql")

@mcp.tool()
async def query_db(query: str) -> dict:
    """Fake database query."""
    if "top" in query.lower():
        return {
            "columns": ["product", "revenue"],
            "rows": [["Product A", 1000], ["Product B", 950]]
        }
    return {"error": "Query not understood."}

# Setup SSE transport (2-way: /messages for POST, /sse for GET)
sse = SseServerTransport("/messages")

# ASGI-style handler for SSE connection
async def handle_sse(scope, receive, send):
    async with sse.connect_sse(scope, receive, send) as streams:
        await mcp.run(
            input=streams[0],
            output=streams[1],
            initialization_options=mcp.create_initialization_options()
        )

# ASGI-style handler for POST JSON-RPC messages
async def handle_messages(scope, receive, send):
    await sse.handle_post_message(scope, receive, send)

# Health check (normal Starlette endpoint)
async def health(request: Request):
    return JSONResponse({"status": "ok"})

# Define the Starlette app with ASGI mounts
app = Starlette(
    routes=[
        Mount("/sse", app=handle_sse),              # ✅ ASGI app
        Mount("/messages", app=handle_messages),    # ✅ ASGI app
    ]
)

# Add standard route via middleware if needed
@app.route("/health")
async def health_route(request: Request):
    return await health(request)