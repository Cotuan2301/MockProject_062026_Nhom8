from django.urls import path
from . import views

app_name = 'medical'

urlpatterns = [
    path('assessments/<int:assessment_id>/loc/', views.loc_classification_detail, name='loc_detail'),
    path('assessments/<int:assessment_id>/loc/confirm/', views.loc_classification_confirm, name='loc_confirm'),
    path('assessments/<int:assessment_id>/loc/override/', views.loc_classification_override, name='loc_override'),
]