from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from flights.models import Seat
from .models import Booking


class BookingService:
    @staticmethod
    @transaction.atomic
    def create_booking(*, flight, passenger, seat_id, tariff, cashier, baggage_weight_kg=0):
        # select_for_update блокирует строку места в БД до конца транзакции —
        # это и есть защита от одновременного бронирования одного места двумя кассирами
        seat = Seat.objects.select_for_update().get(id=seat_id, flight=flight)

        if not seat.is_free():
            raise ValidationError("Это место уже занято или временно заблокировано другим кассиром.")

        if flight.is_departed():
            raise ValidationError("Нельзя оформить билет на рейс, который уже вылетел.")

        total_price = tariff.base_cost
        if baggage_weight_kg > flight.aircraft_type.max_baggage_kg:
            raise ValidationError(
                f"Превышен допустимый вес багажа для {flight.aircraft_type} "
                f"(максимум {flight.aircraft_type.max_baggage_kg} кг)."
            )

        seat.block(cashier)

        booking = Booking.objects.create(
            flight=flight,
            passenger=passenger,
            seat=seat,
            tariff=tariff,
            cashier=cashier,
            baggage_weight_kg=baggage_weight_kg,
            total_price=total_price,
        )
        return booking