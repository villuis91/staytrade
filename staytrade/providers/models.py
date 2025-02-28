from staytrade.shared.abstract_models import TimeStampedModel
from staytrade.users.models import User, EnterpriseAccount
from django.db import models


class Hotel(TimeStampedModel):
    class HotelTypes(models.TextChoices):
        PROVIDER = "provider", _("Provider")
        TRADER = "trader", _("Trader")

    user = models.ForeignKey(User)
    account = models.ForeignKey(
        EnterpriseAccount, blank=True, null=True, on_delete=models.SET_NULL
    )
    description = models.TextField()
    stars = models.IntegerField()


class RoomTypes(TimeStampedModel):
    pass


class Rooms(TimeStampedModel):
    pass


class RoomNight(TimeStampedModel):
    pass
