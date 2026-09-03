from django.db import models
from accounts.models import Cashier


class AuditLog(models.Model):
    user = models.ForeignKey(
        Cashier, on_delete=models.SET_NULL, null=True, blank=True, related_name="audit_logs"
    )
    action = models.CharField(max_length=50, verbose_name="Действие")
    object_repr = models.CharField(max_length=255, verbose_name="Объект")
    details = models.TextField(blank=True, verbose_name="Подробности")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Запись журнала аудита"
        verbose_name_plural = "Журнал аудита"
        ordering = ["-created_at"]

    def __str__(self):
        who = self.user.username if self.user else "система"
        return f"[{self.created_at:%Y-%m-%d %H:%M}] {who}: {self.action} — {self.object_repr}"