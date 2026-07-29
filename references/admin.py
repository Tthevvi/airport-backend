from django.contrib import admin
from .models import Airport, Direction, AircraftType, Tariff


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "city", "country")
    search_fields = ("code", "name", "city")


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ("__str__", "distance_km")
    list_filter = ("departure_airport", "arrival_airport")


@admin.register(AircraftType)
class AircraftTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "capacity", "max_baggage_kg")
    list_filter = ("category",)


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ("direction", "aircraft_type", "travel_class", "base_cost", "refundable")
    list_filter = ("travel_class", "refundable")