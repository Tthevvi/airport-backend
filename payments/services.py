import uuid
from django.db import transaction
from rest_framework.exceptions import ValidationError

from bookings.models import Booking
from shifts.models import Shift
from .models import Payment
from audit.services import log_action


class PaymentService:
    @staticmethod
    @transaction.atomic
    def pay_booking(*, booking: Booking, shift: Shift, method: str):
        if booking.status == Booking.Status.CONFIRMED:
            raise ValidationError("Бронирование уже оплачено.")
        if shift.status != Shift.Status.OPEN:
            raise ValidationError("Оплата возможна только в рамках открытой смены.")

        payment = Payment.objects.create(
            booking=booking,
            shift=shift,
            method=method,
            amount=booking.total_price,
            fiscal_receipt_no=f"FR-{uuid.uuid4().hex[:10].upper()}",
        )
        booking.confirm()
        log_action(shift.cashier, "payment_created", payment, f"Сумма: {payment.amount}")
        return payment