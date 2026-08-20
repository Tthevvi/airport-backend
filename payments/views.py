from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from bookings.models import Booking
from shifts.models import Shift
from config.utils import get_object_or_400
from .models import Payment
from .serializers import PaymentSerializer, PaymentCreateSerializer
from .services import PaymentService


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related("booking", "shift").all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        input_serializer = PaymentCreateSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        data = input_serializer.validated_data

        booking = get_object_or_400(Booking, id=data["booking_id"])
        shift = get_object_or_400(Shift, id=data["shift_id"])

        payment = PaymentService.pay_booking(booking=booking, shift=shift, method=data["method"])
        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)