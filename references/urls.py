from rest_framework.routers import DefaultRouter
from .views import AirportViewSet, DirectionViewSet, AircraftTypeViewSet, TariffViewSet

router = DefaultRouter()
router.register("airports", AirportViewSet)
router.register("directions", DirectionViewSet)
router.register("aircraft-types", AircraftTypeViewSet)
router.register("tariffs", TariffViewSet)

urlpatterns = router.urls