from django.urls import path
from .views import ResidentDetailAPIView, ResidentCreateUpdateAPIView

urlpatterns = [
    path('<int:pk>/', ResidentDetailAPIView.as_view(), name='resident-detail'),
    path('create/', ResidentCreateUpdateAPIView.as_view(), name='resident-create'),
    path('edit/<int:pk>/', ResidentCreateUpdateAPIView.as_view(), name='resident-edit'),
]

