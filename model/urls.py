from django.urls import path

from .views import pivot
from .views import interface
from .views import chat
from .views import modal

app_name = 'model'

urlpatterns = [
    path('', interface.index, name='index'),
    path('run_sql/', interface.run_sql, name='run_sql'),
    path('receive_assist_prompt/', chat.receive_assist_prompt, name='receive_assist_prompt'),
    path('pivot/', pivot.index, name='pivot'),
    path('receive_pivot_fields/', pivot.receive_pivot_fields, name='receive_pivot_fields'),
    path('show_modal/', modal.show_modal, name='show_modal'),
    path('close_modal/', modal.close_modal, name='close_modal'),
]