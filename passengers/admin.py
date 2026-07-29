from django.contrib import admin
from .models import Passenger


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ("full_name", "passport_series", "passport_number", "phone", "email")
    search_fields = ("last_name", "first_name", "passport_series", "passport_number")