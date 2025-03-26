import asyncio
from client import MCPClient

async def main():
    async with MCPClient("http://127.0.0.1:8000") as client:
        tools = await client.list_tools()
        print("Available tools:")
        for tool in tools:
            print(f"- {tool['name']}: {tool['description']}")

        # Run the query_db tool
        print("\nRunning tool `query_db`...\n")
        await client.process_query("query_db", {"query": "SELECT top 10 from products"})

asyncio.run(main())