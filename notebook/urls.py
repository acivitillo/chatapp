from django.urls import path
from . import views

app_name = 'notebook'

urlpatterns = [
    path('', views.index, name='notebook_index'),
    path('new-cell/', views.new_cell, name='new_cell'),
    path('send/', views.send, name='send'),
    path('sidebar/mcp-tree/', views.mcp_tree, name='mcp_tree'),
] 