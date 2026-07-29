from django.db import models
from django.utils import timezone

from bookings.models import Booking
from accounts.models import Cashier


class Refund(models.Model):
    class Reason(models.TextChoices):
        VOLUNTARY = "voluntary", "Добровольный"
        FORCED = "forced", "Вынужденный"

    booking = models.OneToOneField(Booking, on_delete=models.PROTECT, related_name="refund")
    cashier = models.ForeignKey(Cashier, on_delete=models.PROTECT, related_name="refunds")
    reason = models.CharField(max_length=20, choices=Reason.choices)
    penalty_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)
    refund_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Возврат"
        verbose_name_plural = "Возвраты"
        ordering = ["-refund_date"]

    def __str__(self):
        return f"Возврат по {self.booking} ({self.get_reason_display()})"

    def is_voluntary(self) -> bool:
        return self.reason == self.Reason.VOLUNTARY

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            self.booking.cancel()