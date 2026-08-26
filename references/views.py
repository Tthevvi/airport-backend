from rest_framework import viewsets, permissions
from accounts.permissions import IsAdminRole
from .models import Airport, Direction, AircraftType, Tariff
from .serializers import AirportSerializer, DirectionSerializer, AircraftTypeSerializer, TariffSerializer


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminRole]


class DirectionViewSet(viewsets.ModelViewSet):
    queryset = Direction.objects.select_related("departure_airport", "arrival_airport").all()
    serializer_class = DirectionSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminRole]


class AircraftTypeViewSet(viewsets.ModelViewSet):
    queryset = AircraftType.objects.all()
    serializer_class = AircraftTypeSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminRole]


class TariffViewSet(viewsets.ModelViewSet):
    queryset = Tariff.objects.select_related("direction", "aircraft_type").all()
    serializer_class = TariffSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminRole]