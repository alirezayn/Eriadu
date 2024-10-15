from rest_framework import serializers
from.models import UserToken

class NotificationSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)
    title = serializers.CharField(max_length=255)
    body = serializers.CharField(max_length=255)

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserToken
        fields = ['user', 'token']
