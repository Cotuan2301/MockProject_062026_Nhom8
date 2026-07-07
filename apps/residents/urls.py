from django.urls import path
from . import views

app_name = 'residents'
urlpatterns = [
    path('add_resident/', views.add_resident, name="add_resident"),
]