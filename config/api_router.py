from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from staytrade.users.api.views import UserViewSet
from staytrade.providers.api.views import RoomPriceViewSet
from staytrade.reservations.api.views import RoomNightViewSet, BookingViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register(r"room-prices", RoomPriceViewSet, basename="room-prices")
router.register(r'room-nights', RoomNightViewSet)
router.register(r'bookings', BookingViewSet)

app_name = "api"
urlpatterns = router.urls
