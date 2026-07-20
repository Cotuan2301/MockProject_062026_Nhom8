from django.urls import path, include
from . import views

app_name = 'medical'
urlpatterns = [
    path('assessments/<int:assessment_id>/loc/', views.loc_classification_detail, name='loc_detail'),
    path('assessments/<int:assessment_id>/loc/confirm/', views.loc_classification_confirm, name='loc_confirm'),
    path('assessments/<int:assessment_id>/loc/override/', views.loc_classification_override, name='loc_override'),

    path('api/', include('apps.medical.api.urls')),
    path('residents/<int:resident_id>/loc-history/', views.loc_history_view, name='loc-history'),
  
    path('screenings/create/<int:resident_id>/', views.ScreeningCreate.as_view(), name='screening-create'),
    path('admission-form/<int:resident_id>/', views.AdmissionFormView.as_view(), name='admission-form'),
]