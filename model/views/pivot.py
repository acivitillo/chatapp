import os
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import sqlite3
import pandas as pd
from io import StringIO
import sqlparse
# hook for the generate_sql module
from ai.modules.sql import generate_sql
from utils import get_df_from_sql

@csrf_exempt
def index(request):
    sql = "SELECT * FROM Invoice"
    df = get_df_from_sql(sql)
    return render(request, 'pivot/index.html', {"df": df})

@csrf_exempt
def receive_pivot_fields(request):
    if request.method == 'POST':
        try:
            # Parse the JSON strings from form data
            rows = json.loads(request.POST.get('rows', '[]'))
            columns = json.loads(request.POST.get('columns', '[]'))
            values = json.loads(request.POST.get('values', '[]'))

            # Build the SQL query
            select_cols = rows + [f'SUM({val}) as {val}_sum' for val in values]
            
            # Generate initial SQL string
            sql = f"""
            SELECT {', '.join(select_cols)}
            FROM Invoice
            GROUP BY {', '.join(columns)}
            """
            
            # Format the SQL string for better readability
            sql = sqlparse.format(
                sql,
                reindent=True,
                keyword_case='upper',
                strip_comments=True,
                use_space_around_operators=True
            )
            request.session['sql'] = sql
            # Get the pivoted data
            df = get_df_from_sql(sql)
            
            # Make sure to include the SQL in the context
            context = {
                'df': df,
                'sql': sql,
                'group_by_cols': columns,
            }
            return render(request, 'pivot/refreshed_table.html', context)
        except json.JSONDecodeError as e:
            print("JSON decode error:", str(e))
            print("Raw POST data:", request.POST)
            return HttpResponse("Invalid JSON data", status=400)
        except Exception as e:
            print("Error:", str(e))
            return HttpResponse(str(e), status=400)
    return HttpResponse("Invalid request method", status=405)


