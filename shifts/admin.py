from django.contrib import admin
from .models import Shift


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ("id", "cashier", "status", "open_time", "close_time", "cash_total", "card_total")
    list_filter = ("status", "cashier")