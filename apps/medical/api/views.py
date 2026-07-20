from rest_framework import viewsets

from apps.medical.models import CareLevel, CarePlan, CareGoal
from .serializers import (
    CareLevelSerializer,
    CarePlanSerializer,
    CareGoalSerializer,
)


class CareLevelViewSet(viewsets.ModelViewSet):
    queryset = CareLevel.objects.all()
    serializer_class = CareLevelSerializer


class CarePlanViewSet(viewsets.ModelViewSet):
    queryset = CarePlan.objects.all()
    serializer_class = CarePlanSerializer


class CareGoalViewSet(viewsets.ModelViewSet):
    queryset = CareGoal.objects.all()
    serializer_class = CareGoalSerializer