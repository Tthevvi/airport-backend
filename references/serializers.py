from rest_framework import serializers
from .models import Airport, Direction, AircraftType, Tariff


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = "__all__"


class DirectionSerializer(serializers.ModelSerializer):
    departure_airport_name = serializers.CharField(source="departure_airport.city", read_only=True)
    arrival_airport_name = serializers.CharField(source="arrival_airport.city", read_only=True)

    class Meta:
        model = Direction
        fields = "__all__"


class AircraftTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AircraftType
        fields = "__all__"


class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = "__all__"