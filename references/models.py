from django.db import models


class Airport(models.Model):
    code = models.CharField(max_length=3, primary_key=True, verbose_name="Код ИАТА")
    name = models.CharField(max_length=200, verbose_name="Название")
    city = models.CharField(max_length=100, verbose_name="Город")
    country = models.CharField(max_length=100, verbose_name="Страна")

    class Meta:
        verbose_name = "Аэропорт"
        verbose_name_plural = "Аэропорты"

    def __str__(self):
        return f"{self.code} — {self.city}"


class Direction(models.Model):
    departure_airport = models.ForeignKey(
        Airport, on_delete=models.PROTECT, related_name="departures",
        verbose_name="Аэропорт отправления",
    )
    arrival_airport = models.ForeignKey(
        Airport, on_delete=models.PROTECT, related_name="arrivals",
        verbose_name="Аэропорт прибытия",
    )
    distance_km = models.PositiveIntegerField(verbose_name="Расстояние, км")

    class Meta:
        verbose_name = "Направление"
        verbose_name_plural = "Направления"
        constraints = [
            models.CheckConstraint(
                check=~models.Q(departure_airport=models.F("arrival_airport")),
                name="departure_ne_arrival",
            )
        ]

    def __str__(self):
        return f"{self.departure_airport.code} → {self.arrival_airport.code}"


class AircraftType(models.Model):
    class Category(models.TextChoices):
        PLANE = "plane", "Самолёт"
        HELICOPTER = "helicopter", "Вертолёт"

    name = models.CharField(max_length=100, verbose_name="Название")
    category = models.CharField(max_length=20, choices=Category.choices, verbose_name="Категория")
    capacity = models.PositiveSmallIntegerField(verbose_name="Вместимость")
    max_baggage_kg = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Макс. вес багажа, кг")

    class Meta:
        verbose_name = "Тип ВС"
        verbose_name_plural = "Типы ВС"

    def __str__(self):
        return self.name

    def is_helicopter(self) -> bool:
        return self.category == self.Category.HELICOPTER


class Tariff(models.Model):
    class TravelClass(models.TextChoices):
        ECONOMY = "economy", "Эконом"
        BUSINESS = "business", "Бизнес"

    direction = models.ForeignKey(Direction, on_delete=models.PROTECT, related_name="tariffs")
    aircraft_type = models.ForeignKey(AircraftType, on_delete=models.PROTECT, related_name="tariffs")
    travel_class = models.CharField(max_length=20, choices=TravelClass.choices, verbose_name="Класс")
    base_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Базовая стоимость")
    refund_penalty_pct = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="% штрафа за возврат")
    refundable = models.BooleanField(default=True, verbose_name="Возвратность")
    valid_from = models.DateField(verbose_name="Дата начала действия")
    valid_to = models.DateField(verbose_name="Дата окончания действия")

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"

    def __str__(self):
        return f"{self.direction} / {self.aircraft_type} / {self.get_travel_class_display()}"

    def is_active(self, on_date=None) -> bool:
        from django.utils import timezone
        on_date = on_date or timezone.now().date()
        return self.valid_from <= on_date <= self.valid_to