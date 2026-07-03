from django.urls import path
from . import views

app_name = 'residents'

urlpatterns = [
    path('pre-admission/', views.pre_admission, name='pre_admission'),
]
