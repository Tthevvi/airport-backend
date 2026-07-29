from django.contrib.auth.models import AbstractUser
from django.db import models


class Cashier(AbstractUser):
    class Role(models.TextChoices):
        CASHIER = "cashier", "Кассир-оператор"
        SENIOR_CASHIER = "senior_cashier", "Старший кассир"
        ADMIN = "admin", "Администратор"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CASHIER,
        verbose_name="Роль",
    )

    class Meta:
        verbose_name = "Кассир"
        verbose_name_plural = "Кассиры"

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"