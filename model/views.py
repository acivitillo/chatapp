import os
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import sqlite3
import pandas as pd
from io import StringIO

# Create your views here.

def index(request):
    # Option 1: If the file is in templates/model/
    md_file_path = os.path.join(settings.BASE_DIR, 'model', 'templates', 'model', 'default.md')
    
    try:
        with open(md_file_path, 'r', encoding='utf-8') as file:
            markdown_content = file.read()
    except FileNotFoundError:
        markdown_content = "# Welcome to the Model Editor\n\nStart writing your SQL here..."

    sql_file_path = os.path.join(settings.BASE_DIR, 'model', 'templates', 'model', 'sample.sql')
    try:
        with open(sql_file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
    except FileNotFoundError:
        sql_content = "SELECT * FROM table1;"
    print(sql_content)
    return render(request, 'model/index.html', {
        'initial_content': markdown_content,
        'sql_content': sql_content
    })

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
            
            # Connect to SQLite database
            conn = sqlite3.connect('db.sqlite3')
            
            # Execute query and get results as DataFrame
            db_path = os.path.join(settings.BASE_DIR, 'chinook.sqlite')
            conn = sqlite3.connect(db_path)
            df = pd.read_sql_query(sql, conn)
            conn.close()
            return render(request, 'model/table.html', {'df': df})
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=400)
    return HttpResponse("Invalid request method", status=405)

@csrf_exempt
def receive_assist_prompt(request):
    if request.method == 'POST':
        prompt = "--"
        prompt += request.POST.get('message', '')
        # TODO: Implement the logic to generate SQL using AI
        sql = "SELECT * FROM Invoice;"
        response = prompt + "\n" + sql
        return HttpResponse(response)