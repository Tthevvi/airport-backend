from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Flight, Seat
from .serializers import FlightListSerializer, FlightDetailSerializer, SeatSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.select_related("direction", "aircraft_type").all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["direction", "aircraft_type", "departure_date", "status"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return FlightDetailSerializer
        return FlightListSerializer

    @action(detail=True, methods=["get"])
    def seats(self, request, pk=None):
        flight = self.get_object()
        serializer = SeatSerializer(flight.seats.all(), many=True)
        return Response(serializer.data)