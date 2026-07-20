from django.urls import path
from .views import CarePlanListView

app_name = 'care_planning'

urlpatterns = [
    path('care-plans/', CarePlanListView.as_view(), name='care_plan_list'),
]
