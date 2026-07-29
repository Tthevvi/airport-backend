from django.contrib import admin
from .models import Refund


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ("booking", "cashier", "reason", "penalty_amount", "refund_amount", "refund_date")
    list_filter = ("reason",)