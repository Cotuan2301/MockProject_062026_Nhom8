from django.urls import path
from . import views

urlpatterns = [
    path('residents/<int:resident_id>/loc-history/', views.ResidentCareLevelHistoryListView.as_view(), name='loc-history-list'),
    path('residents/<int:resident_id>/loc-history/export/', views.ResidentCareLevelHistoryExportView.as_view(), name='loc-history-export'),
]