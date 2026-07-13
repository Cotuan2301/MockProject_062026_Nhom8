from django.urls import path
from . import views

app_name = 'medical'

urlpatterns = [
    path(
        'initial-assessment/<int:pk>/',
        views.initial_assessment,
        name='initial_assessment',
    ),
    path(
        'initial-assessment/<int:pk>/<int:assessment_id>/',
        views.initial_assessment,
        name='initial_assessment',
    ),
    path(
        'api/assessment/<int:assessment_id>/diagnosis/add/',
        views.api_add_diagnosis,
        name='api_add_diagnosis',
    ),
    path(
        'api/assessment/<int:assessment_id>/diagnosis/<int:diagnosis_id>/remove/',
        views.api_remove_diagnosis,
        name='api_remove_diagnosis',
    ),
]