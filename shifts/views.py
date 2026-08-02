from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Shift
from .serializers import ShiftSerializer
from .services import ShiftService


class ShiftViewSet(viewsets.ModelViewSet):
    queryset = Shift.objects.select_related("cashier").all()
    serializer_class = ShiftSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["post"])
    def open(self, request):
        shift = ShiftService.open_shift(request.user)
        return Response(ShiftSerializer(shift).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def close(self, request, pk=None):
        shift = self.get_object()
        ShiftService.close_shift(shift, request.user)
        return Response(ShiftSerializer(shift).data)

    @action(detail=True, methods=["get"], url_path="x-report")
    def x_report(self, request, pk=None):
        shift = self.get_object()
        return Response(self._build_report(shift))

    @action(detail=True, methods=["get"], url_path="z-report")
    def z_report(self, request, pk=None):
        shift = self.get_object()
        if shift.status != Shift.Status.CLOSED:
            return Response({"detail": "Z-отчёт доступен только для закрытой смены."}, status=400)
        return Response(self._build_report(shift))

    def _build_report(self, shift):
        from django.db.models import Sum, Count
        payments = shift.payments.all()
        by_method = payments.values("method").annotate(total=Sum("amount"), count=Count("id"))
        return {
            "shift_id": shift.id,
            "cashier": shift.cashier.get_full_name(),
            "status": shift.status,
            "total_payments": payments.count(),
            "total_amount": payments.aggregate(Sum("amount"))["amount__sum"] or 0,
            "by_method": list(by_method),
        }