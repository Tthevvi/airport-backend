from rest_framework.routers import DefaultRouter
from .views import RefundViewSet

router = DefaultRouter()
router.register("refunds", RefundViewSet)

urlpatterns = router.urls