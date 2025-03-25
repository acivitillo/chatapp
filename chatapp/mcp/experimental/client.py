import aiohttp
import asyncio
import uuid

class MCPClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url.rstrip("/")
        self.session = None
        self.client_id = str(uuid.uuid4())  # Optional: used for server session tracking

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def list_tools(self):
        """Request list of available tools."""
        payload = {
            "jsonrpc": "2.0",
            "id": "1",
            "method": "list_tools"
        }
        print("Sending payload:", payload)  # 👈 Add this
        async with self.session.post(f"{self.base_url}/messages", json=payload) as resp:
            print("Status:", resp.status)
            print("Raw text:", await resp.text())
            resp.raise_for_status()
            result = await resp.json()
            return result.get("result", {}).get("tools", [])

    async def run_tool(self, tool_name: str, parameters: dict, request_id: str = "2"):
        """Send run_tool request."""
        payload = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": "run_tool",
            "params": {
                "name": tool_name,
                "parameters": parameters
            }
        }
        async with self.session.post(f"{self.base_url}/messages", json=payload) as resp:
            resp.raise_for_status()

    async def stream(self):
        """Connect to /sse and stream all responses."""
        async with self.session.get(f"{self.base_url}/sse") as resp:
            if resp.status != 200:
                raise Exception(f"SSE stream failed: {resp.status}")
            async for line in resp.content:
                decoded = line.decode().strip()
                if decoded.startswith("data:"):
                    print(decoded.removeprefix("data:").strip())

    async def process_query(self, tool_name: str, parameters: dict):
        """High-level function to run a tool and stream the response."""
        await self.run_tool(tool_name, parameters)
        await self.stream()
