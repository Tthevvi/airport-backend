from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("booking_number", "passenger", "flight", "seat", "status", "total_price", "created_at")
    list_filter = ("status", "flight")
    search_fields = ("booking_number", "passenger__last_name")
    readonly_fields = ("booking_number", "created_at")