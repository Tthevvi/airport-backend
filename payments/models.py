from django.db import models

from bookings.models import Booking
from shifts.models import Shift


class Payment(models.Model):
    class Method(models.TextChoices):
        CASH = "cash", "Наличные"
        CARD = "card", "Безналичный расчёт"

    booking = models.ForeignKey(Booking, on_delete=models.PROTECT, related_name="payments")
    shift = models.ForeignKey(Shift, on_delete=models.PROTECT, related_name="payments")
    method = models.CharField(max_length=10, choices=Method.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    fiscal_receipt_no = models.CharField(max_length=30, blank=True)
    paid_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"
        ordering = ["-paid_at"]

    def __str__(self):
        return f"Оплата {self.amount} ({self.get_method_display()}) — {self.booking}"