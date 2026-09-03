from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("references.urls")),
    path("api/token/", obtain_auth_token),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/", include("flights.urls")),
    path("api/", include("passengers.urls")),
    path("api/", include("bookings.urls")),
    path("api/", include("shifts.urls")),
    path("api/", include("payments.urls")),
    path("api/", include("refunds.urls")),
    path("api/", include("accounts.urls")),
    path("api/", include("audit.urls")),
]
