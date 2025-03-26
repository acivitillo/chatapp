import markdown
import textwrap
import uuid

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

chat_history = []  # Temp store

@csrf_exempt
async def index(request):
    return render(request, 'index.html')