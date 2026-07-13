from django.urls import path
from . import views

app_name = 'medical'
urlpatterns = [
    path('reassessments/', views.reassessments, name='reassessments'),
]