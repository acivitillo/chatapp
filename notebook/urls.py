from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='notebook_index'),
    path('new-cell/', views.new_cell, name='new_cell'),
    path('send/', views.send, name='send'),
] 