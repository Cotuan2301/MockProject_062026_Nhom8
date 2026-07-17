from django.urls import path
from .views import ResidentDetailAPIView


urlpatterns = [
    path('<int:pk>/', ResidentDetailAPIView.as_view(), name='resident-detail'),
]

