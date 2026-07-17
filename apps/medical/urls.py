from django.urls import path
from . import views

app_name = 'medical'
urlpatterns = [
    path('daily-tasks/', views.daily_tasks, name='daily_tasks'),
    path('api/update-task/', views.update_task_status, name='update_task_status'),
]