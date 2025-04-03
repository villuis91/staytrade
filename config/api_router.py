from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from staytrade.users.api.views import UserViewSet
from staytrade.providers.api.views import RoomTypeMealPlanPriceViewSet


router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register(r"room-prices", RoomTypeMealPlanPriceViewSet, basename="room-prices")

app_name = "api"
urlpatterns = router.urls
