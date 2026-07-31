from rest_framework import viewsets, permissions, filters
from .models import Passenger
from .serializers import PassengerSerializer


class PassengerViewSet(viewsets.ModelViewSet):
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["last_name", "first_name", "passport_series", "passport_number"]