from rest_framework.routers import DefaultRouter
from .views import ShiftViewSet

router = DefaultRouter()
router.register("shifts", ShiftViewSet)

urlpatterns = router.urls