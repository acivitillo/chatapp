import markdown
import textwrap
import uuid

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .mcp.client import MCPClient

chat_history = []  # Temp store


def index(request):
    return render(request, 'index.html', {'messages': chat_history})


@csrf_exempt
async def send_message(request):
    user_input = request.POST.get("message", "").strip()
    cell_id = request.POST.get("cell_id")
    if not user_input:
        return HttpResponse("Empty input", status=400)

    client = MCPClient()
    await client.connect()
    try:
        response_message = await client.process_query(user_input)
        
        # Process code and determine language if present
        code = response_message.get("code", "")
        code_language = 'text'
        
        if code:
            # Simple language detection based on file extension or content
            if code.startswith('```python') or code.endswith('.py'):
                code_language = 'python'
            elif code.startswith('```html') or code.startswith('<'):
                code_language = 'markup'
            
            # Clean up code content by removing markdown code blocks if present
            if code.startswith('```'):
                lines = code.split('\n')
                code = '\n'.join(lines[1:-1] if lines[-1] == '```' else lines[1:])
    finally:
        await client.close()
        
    return render(request, "output_cell.html", {
        'message': response_message["text"],
        'tool_name': response_message["tool_name"],
        'cell_id': cell_id,
        'code': code,
        'code_language': code_language
    })

@csrf_exempt
async def new_input_cell(request):
    return render(request, "input_cell.html", {
        'cell_id': str(uuid.uuid4())
    })

@csrf_exempt
async def mcp_tree_view(request):
    # Replace this with your actual MCP connection state
    client = MCPClient()
    async with MCPClient() as client:
        tools = await client.tools()
    #print("TOOOLS", tools)
    #This only supports 1 server, needs improvement
    tool_stanzas = []
    for tool in tools:
        name = tool["function"]["name"]
        raw_description = tool["function"]["description"]
        description = textwrap.dedent(raw_description).strip()
        description = markdown.markdown(description)
        print(description)
        parameters = tool["function"]["parameters"]["properties"]
        d = {"name": name, "parameters": parameters
             , "description":description, "raw_description": raw_description}
        tool_stanzas.append(d)
    return render(request, "mcp_tree.html", {"tools": tool_stanzas})