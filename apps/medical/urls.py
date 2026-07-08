from django.urls import path
from . import views

app_name = 'medical'
urlpatterns = [
    path('bedside-vitals/', views.bedside_vitals, name='bedside_vitals'),
]