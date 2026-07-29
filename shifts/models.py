from django.db import models
from django.utils import timezone

from accounts.models import Cashier


class Shift(models.Model):
    class Status(models.TextChoices):
        OPEN = "open", "Открыта"
        CLOSED = "closed", "Закрыта"

    cashier = models.ForeignKey(Cashier, on_delete=models.PROTECT, related_name="shifts")
    open_time = models.DateTimeField(default=timezone.now)
    close_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    cash_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    card_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    z_report_number = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = "Кассовая смена"
        verbose_name_plural = "Кассовые смены"
        ordering = ["-open_time"]

    def __str__(self):
        return f"Смена #{self.pk} ({self.cashier}, {self.get_status_display()})"

    def close(self):
        from django.db.models import Sum
        totals = self.payments.aggregate(
            cash=Sum("amount", filter=models.Q(method="cash")),
            card=Sum("amount", filter=models.Q(method="card")),
        )
        self.cash_total = totals["cash"] or 0
        self.card_total = totals["card"] or 0
        self.close_time = timezone.now()
        self.status = self.Status.CLOSED
        self.save()