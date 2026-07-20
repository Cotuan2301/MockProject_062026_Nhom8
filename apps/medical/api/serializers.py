from rest_framework import serializers
from apps.medical.models import CareLevel, CarePlan, CareGoal


class CareLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareLevel
        fields = "__all__"


class CarePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarePlan
        fields = "__all__"


class CareGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareGoal
        fields = "__all__"