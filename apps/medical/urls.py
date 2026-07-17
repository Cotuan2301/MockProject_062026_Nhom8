from django.urls import path
from . import views

app_name = 'medical'

urlpatterns = [
    path('screenings/create/<int:resident_id>/', views.ScreeningCreate.as_view(), name='screening-create'),
    path('admission-form/<int:resident_id>/', views.AdmissionFormView.as_view(), name='admission-form'),
]