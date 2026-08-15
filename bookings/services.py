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
    @staticmethod
    @transaction.atomic
    def transfer_booking(*, booking, new_flight, new_seat_id):
        if booking.status == Booking.Status.CANCELLED:
            raise ValidationError("Нельзя перенести отменённую бронь.")
        if new_flight.is_departed():
            raise ValidationError("Нельзя перенести на рейс, который уже вылетел.")

        new_seat = Seat.objects.select_for_update().get(id=new_seat_id, flight=new_flight)
        if not new_seat.is_free():
            raise ValidationError("Выбранное место на новом рейсе уже занято.")

        old_seat = booking.seat
        old_status = booking.status

        old_seat.release()

        new_seat.status = Seat.Status.SOLD if old_status == Booking.Status.CONFIRMED else Seat.Status.BLOCKED
        if new_seat.status == Seat.Status.BLOCKED:
            new_seat.block(booking.cashier)
        else:
            new_seat.save()

        booking.flight = new_flight
        booking.seat = new_seat
        booking.save()
        return booking