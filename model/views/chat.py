from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render

from ai.modules.sql import generate_sql

@csrf_exempt
def receive_assist_prompt(request):
    if request.method == 'POST':
        message = request.POST.get('message', '')

        prompt = message
        sql = generate_sql(prompt) # this is a hook for the generate_sql module
        # Return the wrapped message in a styled div
        return render(request, 'chat/message_response.html', {'message': message})
    return HttpResponse("Invalid request", status=400)