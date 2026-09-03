from decimal import Decimal

from django.db import transaction
from rest_framework.exceptions import ValidationError

from bookings.models import Booking
from .models import Refund
from audit.services import log_action


class RefundService:
    @staticmethod
    @transaction.atomic
    def create_refund(*, booking: Booking, cashier, reason: str):
        if hasattr(booking, "refund"):
            raise ValidationError("По этой брони возврат уже оформлен.")

        if booking.status == Booking.Status.CANCELLED:
            raise ValidationError("Бронирование уже отменено.")

        tariff = booking.tariff

        if reason == Refund.Reason.FORCED:
            penalty = Decimal("0")
        else:
            if not tariff.refundable:
                raise ValidationError("Тариф невозвратный, добровольный возврат невозможен.")
            penalty = (booking.total_price * tariff.refund_penalty_pct / Decimal("100")).quantize(Decimal("0.01"))

        refund_amount = booking.total_price - penalty

        refund = Refund.objects.create(
            booking=booking,
            cashier=cashier,
            reason=reason,
            penalty_amount=penalty,
            refund_amount=refund_amount,
        )
        refund = Refund.objects.create(...)
        log_action(cashier, "refund_created", refund, f"Штраф: {refund.penalty_amount}")
        return refund