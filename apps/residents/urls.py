from django.urls import path
from .views import *

app_name = 'residents'

urlpatterns = [
    path('add_resident/', add_resident, name="add_resident"),
    
    path('resident_details/<int:pk>/', ResidentDetail.as_view(), name="resident_detail"),
]

