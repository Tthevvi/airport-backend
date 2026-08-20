from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from flights.models import Flight
from passengers.models import Passenger
from references.models import Tariff
from config.utils import get_object_or_400
from .models import Booking
from .serializers import BookingSerializer, BookingCreateSerializer, BookingTransferSerializer
from .services import BookingService

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.select_related("flight", "passenger", "seat", "tariff", "cashier").all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        input_serializer = BookingCreateSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        data = input_serializer.validated_data

        flight = get_object_or_400(Flight, id=data["flight_id"])
        passenger = get_object_or_400(Passenger, id=data["passenger_id"])
        tariff = get_object_or_400(Tariff, id=data["tariff_id"])

        booking = BookingService.create_booking(
            flight=flight,
            passenger=passenger,
            seat_id=data["seat_id"],
            tariff=tariff,
            cashier=request.user,
            baggage_weight_kg=data["baggage_weight_kg"],
        )
        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)


    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        booking.cancel()
        return Response(BookingSerializer(booking).data)
    
    @action(detail=True, methods=["post"])
    def transfer(self, request, pk=None):
        booking = self.get_object()
        input_serializer = BookingTransferSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        data = input_serializer.validated_data

        new_flight = Flight.objects.get(id=data["new_flight_id"])
        booking = BookingService.transfer_booking(
            booking=booking, new_flight=new_flight, new_seat_id=data["new_seat_id"]
        )
        return Response(BookingSerializer(booking).data)