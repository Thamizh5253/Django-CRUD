from django.urls import path
from .views import task_list_create, task_detail

urlpatterns = [
    path('tasks/', task_list_create, name='task_list_create'),
    path('tasks/<int:pk>/', task_detail, name='task_detail'),
]
