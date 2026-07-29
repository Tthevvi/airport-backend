from django.contrib import admin
from .models import Flight, Seat


class SeatInline(admin.TabularInline):
    model = Seat
    extra = 0
    fields = ("seat_number", "travel_class", "status")


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ("flight_number", "direction", "aircraft_type", "departure_date", "departure_time", "status")
    list_filter = ("status", "direction", "aircraft_type")
    search_fields = ("flight_number",)
    inlines = [SeatInline]


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ("flight", "seat_number", "travel_class", "status", "blocked_until")
    list_filter = ("status", "travel_class")