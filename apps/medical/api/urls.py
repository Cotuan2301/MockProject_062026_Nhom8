from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CareLevelViewSet,
    CarePlanViewSet,
    CareGoalViewSet,
)

router = DefaultRouter()
router.register(r"care-levels", CareLevelViewSet)
router.register(r"care-plans", CarePlanViewSet)
router.register(r"care-goals", CareGoalViewSet)

urlpatterns = [
    path("", include(router.urls)),
]