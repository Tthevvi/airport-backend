from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Cashier


@admin.register(Cashier)
class CashierAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Роль", {"fields": ("role",)}),
    )
    list_display = ("username", "get_full_name", "role", "is_staff")