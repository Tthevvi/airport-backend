import uuid
from django.db import models
from django.utils import timezone

from flights.models import Flight, Seat
from passengers.models import Passenger
from references.models import Tariff
from accounts.models import Cashier


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Ожидает оплаты"
        CONFIRMED = "confirmed", "Подтверждено"
        CANCELLED = "cancelled", "Отменено"

    booking_number = models.CharField(max_length=20, unique=True, editable=False, verbose_name="Номер брони")
    flight = models.ForeignKey(Flight, on_delete=models.PROTECT, related_name="bookings")
    passenger = models.ForeignKey(Passenger, on_delete=models.PROTECT, related_name="bookings")
    seat = models.ForeignKey(Seat, on_delete=models.PROTECT, related_name="bookings")
    tariff = models.ForeignKey(Tariff, on_delete=models.PROTECT, related_name="bookings")
    cashier = models.ForeignKey(Cashier, on_delete=models.PROTECT, related_name="bookings")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    baggage_weight_kg = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["seat"],
                condition=models.Q(status__in=["pending", "confirmed"]),
                name="unique_active_booking_per_seat",
            )
        ]

    def __str__(self):
        return f"Бронь {self.booking_number} ({self.passenger})"

    def save(self, *args, **kwargs):
        if not self.booking_number:
            self.booking_number = f"BK-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def validate_baggage(self) -> bool:
        max_allowed = self.flight.aircraft_type.max_baggage_kg
        return self.baggage_weight_kg <= max_allowed

    def confirm(self):
        self.status = self.Status.CONFIRMED
        self.seat.status = Seat.Status.SOLD
        self.seat.save()
        self.save()

    def cancel(self):
        self.status = self.Status.CANCELLED
        self.seat.release()
        self.save()