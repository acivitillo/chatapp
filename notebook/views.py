from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import uuid

from mcpclient.client import MCPClient

def index(request):
    return render(request, 'notebook/index.html')

@csrf_exempt
async def new_cell(request):
    return render(request, "notebook/markdown_cell.html", {
        'cell_id': str(uuid.uuid4())
    })
    
@csrf_exempt
async def send(request):
    user_input = request.POST.get("message", "").strip()
    cell_id = request.POST.get("cell_id")
    if not user_input:
        return HttpResponse("Empty input", status=400)

    client = MCPClient()
    await client.connect()
    try:
        response_message = await client.process_query(user_input)
    finally:
        await client.close()
        
    return render(request, "notebook/output_cell.html", {
        'message': response_message["text"],
        'tool_name': response_message["tool_name"],
        'cell_id': cell_id,
        'code': response_message["code"],
        'code_language': response_message["code_language"],
    })
