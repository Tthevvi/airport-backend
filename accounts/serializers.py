from rest_framework import serializers
from .models import Cashier


class CashierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cashier
        fields = ["id", "username", "first_name", "last_name", "role"]