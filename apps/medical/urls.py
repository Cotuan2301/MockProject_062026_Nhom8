from django.urls import path
from . import views

app_name = 'medical'
urlpatterns = [
    path('reassessments/', views.reassessments, name='reassessments'),
    path('api/start-reassessment/', views.start_reassessment, name='start_reassessment'),
]