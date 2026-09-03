from rest_framework import serializers
from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True, default="система")

    class Meta:
        model = AuditLog
        fields = ["id", "username", "action", "object_repr", "details", "created_at"]