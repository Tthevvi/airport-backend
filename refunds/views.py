from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from bookings.models import Booking
from .models import Refund
from .serializers import RefundSerializer, RefundCreateSerializer
from .services import RefundService


class RefundViewSet(viewsets.ModelViewSet):
    queryset = Refund.objects.select_related("booking", "cashier").all()
    serializer_class = RefundSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        input_serializer = RefundCreateSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        data = input_serializer.validated_data

        booking = Booking.objects.get(id=data["booking_id"])
        refund = RefundService.create_refund(
            booking=booking, cashier=request.user, reason=data["reason"]
        )
        return Response(RefundSerializer(refund).data, status=status.HTTP_201_CREATED)