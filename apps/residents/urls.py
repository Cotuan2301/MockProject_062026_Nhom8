from django.urls import path
from .views import *

app_name = 'residents'

urlpatterns = [
    path('list/', resident_list, name="list"),
    
    path('resident_create/', ResidentCreate.as_view(), name="resident_create"),
    path('resident_details/<int:pk>/', ResidentDetail.as_view(), name="resident_detail"),
    path('resident_edit/<int:pk>/', ResidentEdit.as_view(), name="resident_edit"),
    path('check_similar/', check_similar_resident, name="check_similar"),
]

