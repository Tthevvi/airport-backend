from rest_framework import serializers
from .models import Refund


class RefundCreateSerializer(serializers.Serializer):
    booking_id = serializers.IntegerField()
    reason = serializers.ChoiceField(choices=Refund.Reason.choices)


class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = "__all__"
        read_only_fields = ["cashier", "penalty_amount", "refund_amount", "refund_date"]