from rest_framework import serializers
from .models import Flight, Seat


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ["id", "seat_number", "travel_class", "status", "blocked_until"]


class FlightListSerializer(serializers.ModelSerializer):
    direction_display = serializers.CharField(source="direction.__str__", read_only=True)
    free_seats = serializers.SerializerMethodField()

    class Meta:
        model = Flight
        fields = [
            "id", "flight_number", "direction", "direction_display",
            "aircraft_type", "departure_date", "departure_time",
            "arrival_time", "status", "free_seats",
        ]

    def get_free_seats(self, obj):
        return obj.free_seats_count()


class FlightDetailSerializer(FlightListSerializer):
    seats = SeatSerializer(many=True, read_only=True)

    class Meta(FlightListSerializer.Meta):
        fields = FlightListSerializer.Meta.fields + ["seats"]