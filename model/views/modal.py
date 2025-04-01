from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from utils import get_df_from_sql

@csrf_exempt
def show_modal(request):
    sql = "SELECT * FROM Invoice"
    df = get_df_from_sql(sql)
    return render(request, 'utils/modal.html', {'df': df})

@csrf_exempt
def close_modal(request):
    sql = request.session['sql']  # Get specific 'sql' variable from session
    print(sql)
    return render(request, 'chat/sql_response.html', {'sql': sql})



