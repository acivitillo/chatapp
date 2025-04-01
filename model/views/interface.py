import os
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from utils import get_df_from_sql

def index(request):
    return render(request, 'interface/index.html', {
        'initial_content': "type sql here"})

@csrf_exempt
def run_sql(request):
    if request.method == 'POST':
        try:
            # Try to get SQL from JSON first
            try:
                data = json.loads(request.body)
                sql = data.get('sql', '')
                print(sql)
            except json.JSONDecodeError:
                # If not JSON, try form data
                sql = request.POST.get('sql', '')
            df = get_df_from_sql(sql)
            return render(request, 'utils/table.html', {'df': df})
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=400)
    return HttpResponse("Invalid request method", status=405)
