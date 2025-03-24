import markdown
import textwrap

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
    if not user_input:
        return HttpResponse("Empty input", status=400)

    client = MCPClient()
    await client.connect()
    try:
        response_message = await client.process_query(user_input)
    finally:
        await client.close()
    return render(request, "output_cell.html", {
        'message': response_message["text"],
        'tool_name': response_message["tool_name"],
    })

@csrf_exempt
async def new_input_cell(request):
    return render(request, "input_cell.html")

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