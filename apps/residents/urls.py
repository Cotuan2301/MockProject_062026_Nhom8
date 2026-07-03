from django.urls import path
from . import views

app_name = 'residents'

urlpatterns = [
    path('admission/pre-screening/', views.pre_admission_screening, name='pre_admission_screening'),
]