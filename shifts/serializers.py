from rest_framework import serializers
from .models import Shift


class ShiftSerializer(serializers.ModelSerializer):
    cashier_name = serializers.CharField(source="cashier.get_full_name", read_only=True)

    class Meta:
        model = Shift
        fields = "__all__"
        read_only_fields = ["cashier", "open_time", "close_time", "status", "cash_total", "card_total", "z_report_number"]