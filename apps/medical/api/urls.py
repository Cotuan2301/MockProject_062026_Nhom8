from django.urls import path
from .views import (
    PreAdmissionScreeningDetailAPIView, 
    PreAdmissionScreeningCreateUpdateAPIView, 
    ComplianceCheckAPIView,
    AdmissionCreateAPIView
)

app_name = 'medical_api'

urlpatterns = [
    path('screenings/<int:pk>/', PreAdmissionScreeningDetailAPIView.as_view(), name='screening-detail'),
    path('screenings/create/', PreAdmissionScreeningCreateUpdateAPIView.as_view(), name='screening-create'),
    path('screenings/edit/<int:pk>/', PreAdmissionScreeningCreateUpdateAPIView.as_view(), name='screening-edit'),
    path('screenings/compliance-check/', ComplianceCheckAPIView.as_view(), name='screening-compliance-check'),
    path('admissions/create/', AdmissionCreateAPIView.as_view(), name='admission-create'),
]
