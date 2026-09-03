from rest_framework.exceptions import ValidationError
from .models import Shift
from audit.services import log_action

class ShiftService:
    @staticmethod
    def open_shift(cashier):
        existing_open = Shift.objects.filter(cashier=cashier, status=Shift.Status.OPEN).exists()
        if existing_open:
            raise ValidationError("У вас уже есть открытая смена.")
        shift = Shift.objects.create(cashier=cashier)
        log_action(cashier, "shift_opened", shift)
        return shift

    @staticmethod
    def close_shift(shift, closing_user):
        if shift.status == Shift.Status.CLOSED:
            raise ValidationError("Смена уже закрыта.")
        if closing_user != shift.cashier and closing_user.role != "senior_cashier" and not closing_user.is_superuser:
            raise ValidationError("Недостаточно прав для закрытия чужой смены.")
        shift.close()
        log_action(closing_user, "shift_closed", shift, f"Итого: нал {shift.cash_total}, карта {shift.card_total}")
        return shift
    def perform_create(self, serializer):
        instance = serializer.save()
        log_action(self.request.user, "tariff_created", instance)

    def perform_update(self, serializer):
        instance = serializer.save()
        log_action(self.request.user, "tariff_updated", instance)

    def perform_destroy(self, instance):
        log_action(self.request.user, "tariff_deleted", instance)
        instance.delete()