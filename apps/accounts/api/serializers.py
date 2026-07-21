from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField(required=True, allow_blank=False, max_length=255)
    password = serializers.CharField(required=True, allow_blank=False, trim_whitespace=False, write_only=True)