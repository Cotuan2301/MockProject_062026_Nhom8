from rest_framework import serializers
from apps.medical.models import ResidentCareLevelHistory

class ResidentCareLevelHistorySerializer(serializers.ModelSerializer):
    actor_name = serializers.SerializerMethodField()

    class Meta:
        model = ResidentCareLevelHistory
        fields = [
            'id', 'date', 'action', 'previous_tier', 
            'new_tier', 'actor_name', 'note'
        ]

    def get_actor_name(self, obj):
        if obj.actor:
            return obj.actor.get_full_name() or obj.actor.username
        return "System"