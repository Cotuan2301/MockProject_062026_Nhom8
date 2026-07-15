from django.urls import path, include
from . import views

app_name = 'medical'
urlpatterns = [
    path('api/', include('apps.medical.api.urls')),
    path('residents/<int:resident_id>/loc-history/', views.loc_history_view, name='loc-history'),
]