from rest_framework import serializers
from .models import Booking


class BookingCreateSerializer(serializers.Serializer):
    flight_id = serializers.IntegerField()
    passenger_id = serializers.IntegerField()
    seat_id = serializers.IntegerField()
    tariff_id = serializers.IntegerField()
    baggage_weight_kg = serializers.DecimalField(max_digits=6, decimal_places=2, default=0)


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = ["booking_number", "status", "total_price", "created_at"]