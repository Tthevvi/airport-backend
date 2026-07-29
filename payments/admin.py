from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("booking", "shift", "method", "amount", "paid_at", "fiscal_receipt_no")
    list_filter = ("method", "shift")