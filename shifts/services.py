from rest_framework.exceptions import ValidationError
from .models import Shift


class ShiftService:
    @staticmethod
    def open_shift(cashier):
        existing_open = Shift.objects.filter(cashier=cashier, status=Shift.Status.OPEN).exists()
        if existing_open:
            raise ValidationError("У вас уже есть открытая смена.")
        return Shift.objects.create(cashier=cashier)

    @staticmethod
    def close_shift(shift, closing_user):
        if shift.status == Shift.Status.CLOSED:
            raise ValidationError("Смена уже закрыта.")
        # только сам кассир или старший кассир могут закрыть смену
        if closing_user != shift.cashier and closing_user.role != "senior_cashier" and not closing_user.is_superuser:
            raise ValidationError("Недостаточно прав для закрытия чужой смены.")
        shift.close()
        return shift