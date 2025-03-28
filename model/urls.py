from django.urls import path
from . import views

app_name = 'report'

urlpatterns = [
    path('', views.index, name='index'),
    path('run_sql/', views.run_sql, name='run_sql'),
    path('receive_assist_prompt/', views.receive_assist_prompt, name='receive_assist_prompt'),
] 