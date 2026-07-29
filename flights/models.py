from django.db import models
from django.utils import timezone

from references.models import Direction, AircraftType
from accounts.models import Cashier


class Flight(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Запланирован"
        DEPARTED = "departed", "Вылетел"
        CANCELLED = "cancelled", "Отменён"

    flight_number = models.CharField(max_length=10, unique=True, verbose_name="Номер рейса")
    direction = models.ForeignKey(Direction, on_delete=models.PROTECT, related_name="flights")
    aircraft_type = models.ForeignKey(AircraftType, on_delete=models.PROTECT, related_name="flights")
    departure_date = models.DateField(verbose_name="Дата вылета")
    departure_time = models.TimeField(verbose_name="Время вылета")
    arrival_time = models.TimeField(verbose_name="Время прилёта")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SCHEDULED)

    class Meta:
        verbose_name = "Рейс"
        verbose_name_plural = "Рейсы"
        ordering = ["departure_date", "departure_time"]

    def __str__(self):
        return f"{self.flight_number} ({self.direction}, {self.departure_date})"

    def is_departed(self) -> bool:
        departure_dt = timezone.make_aware(
            timezone.datetime.combine(self.departure_date, self.departure_time)
        )
        return self.status == self.Status.DEPARTED or timezone.now() >= departure_dt

    def free_seats_count(self) -> int:
        return self.seats.filter(status=Seat.Status.FREE).count()

    def occupied_seats_count(self) -> int:
        return self.seats.exclude(status=Seat.Status.FREE).count()


class Seat(models.Model):
    class Status(models.TextChoices):
        FREE = "free", "Свободно"
        BLOCKED = "blocked", "Забронировано временно"
        SOLD = "sold", "Продано"

    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="seats")
    seat_number = models.CharField(max_length=5, verbose_name="Номер места")
    travel_class = models.CharField(max_length=20, verbose_name="Класс")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.FREE)
    blocked_until = models.DateTimeField(null=True, blank=True, verbose_name="Блокировка до")
    blocked_by = models.ForeignKey(
        Cashier, on_delete=models.SET_NULL, null=True, blank=True, related_name="blocked_seats"
    )

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"
        unique_together = ("flight", "seat_number")

    def __str__(self):
        return f"{self.flight.flight_number} / {self.seat_number}"

    def is_free(self) -> bool:
        if self.status == self.Status.FREE:
            return True
        # автоматическое освобождение, если 5-минутная блокировка истекла
        if self.status == self.Status.BLOCKED and self.blocked_until and timezone.now() > self.blocked_until:
            return True
        return False

    def block(self, cashier: Cashier, minutes: int = 5):
        from datetime import timedelta
        self.status = self.Status.BLOCKED
        self.blocked_by = cashier
        self.blocked_until = timezone.now() + timedelta(minutes=minutes)
        self.save()

    def release(self):
        self.status = self.Status.FREE
        self.blocked_by = None
        self.blocked_until = None
        self.save()