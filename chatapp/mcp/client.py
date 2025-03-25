# chatapp/mcp_engine.py
import asyncio
import re
import markdown
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import OpenAI
from contextlib import AsyncExitStack
import os
import json
import subprocess

#configs
from chatapp.config import OPENAI_KEY, SERVER_PATH

DETACHED_PROCESS = subprocess.CREATE_NEW_PROCESS_GROUP  # Or use CREATE_NO_WINDOW if desired



class MCPClient:
    def __init__(self):
        self.session = None
        self.exit_stack = AsyncExitStack()
        self.openai = OpenAI(api_key=OPENAI_KEY)

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.cleanup()

    async def cleanup(self):
        await self.exit_stack.aclose()

    async def connect(self):
        server_path = SERVER_PATH
        server_params = StdioServerParameters(
            command="uv",
            args=["run", server_path],
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        await self.session.initialize()

    async def tools(self) -> list:
        response = await self.session.list_tools()
        available_tools = [{
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema
            }
        } for tool in response.tools]
        return available_tools

    async def process_query(self, query: str) -> str:
        messages = [{"role": "user", "content": query}]
        response = await self.session.list_tools()
        available_tools = [{
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema
            }
        } for tool in response.tools]

        res = self.openai.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=messages,
            tools=available_tools,
            tool_choice="auto"
        )

        message = res.choices[0].message
        response_message = {}
        text = ""

        if message.tool_calls:
            for call in message.tool_calls:
                tool_name = call.function.name
                tool_args = json.loads(call.function.arguments)
                result = await self.session.call_tool(tool_name, tool_args)
                messages.append({"role": "assistant", "tool_calls": [call.model_dump()]})
                messages.append({"role": "tool", "tool_call_id": call.id, "content": result.content})

                text = result.content[0].text
                response_message["tool_name"] = tool_name
        else:
            text = message.content
            response_message["tool_name"] = "no tool used"

        # Check for code blocks in the text
        if re.search(r'<[a-z][\s\S]*>', text, re.IGNORECASE):
            response_message["text"] = text
            response_message["code"] = text
            response_message["code_language"] = "html"
        elif re.search(r'```sql\n[\s\S]*?```', text) or re.search(r'SELECT\s+.*?FROM', text, re.IGNORECASE):
            response_message["text"] = text
            response_message["code"] = text
            response_message["code_language"] = "sql"
        elif (re.search(r'```python\n[\s\S]*?```', text) or 
              re.search(r'def\s+\w+\s*\(', text) or 
              re.search(r'class\s+\w+\s*\(', text) or 
              re.search(r'import\s+\w+', text) or 
              re.search(r'from\s+\w+\s+import', text)):
            response_message["text"] = text
            response_message["code"] = text
            response_message["code_language"] = "python"
        else:
            response_message["text"] = text
            response_message["code"] = ""
            response_message["code_language"] = "text"
        return response_message

    async def close(self):
        await self.exit_stack.aclose()
