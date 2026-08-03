from rest_framework import serializers
from .models import Payment


class PaymentCreateSerializer(serializers.Serializer):
    booking_id = serializers.IntegerField()
    shift_id = serializers.IntegerField()
    method = serializers.ChoiceField(choices=Payment.Method.choices)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ["amount", "fiscal_receipt_no", "paid_at"]