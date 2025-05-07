from django.db import models
from .managers import RoomNightManager, BookingManager
from staytrade.shared.abstract_models import SoftDeletedTimestamped
from staytrade.providers.models import RoomType
from staytrade.users.models import User
from django.utils.translation import gettext_lazy as _


class RoomNightOwner(SoftDeletedTimestamped):
    # Required data to own a RoomNight or booking
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=128)
    phone_number = models.IntegerField()
    national_identifier = models.CharField(max_length=64)
    # If it is registered, link it
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)


# Probably will be dropped from this app and included in the trading one
class RoomNight(SoftDeletedTimestamped):
    entry_date = models.DateField(
        null=False,
        blank=False,
    )
    departure_date = models.DateField(
        null=False,
        blank=False,
    )
    room_type = models.ForeignKey(
        RoomType,
        on_delete=models.DO_NOTHING,
        null=False,
        blank=False,
    )
    # TODO: Null must be removed in production and set a default
    owner = models.ForeignKey(RoomNightOwner, on_delete=models.DO_NOTHING, null=True)
    objects = RoomNightManager()


class Booking(SoftDeletedTimestamped):
    class BookingStatus(models.TextChoices):
        PENDING = "PE", _("Pending")
        CONFIRMED = "CO", _("Confirmed")
        CANCELLED = "CA", _("Cancelled")

    check_in = models.DateTimeField(
        null=False,
        blank=False,
    )
    check_out = models.DateTimeField(
        null=False,
        blank=False,
    )
    status = models.CharField(
        max_length=2, choices=BookingStatus, default=BookingStatus.PENDING
    )
    room_nights = models.ManyToManyField(RoomNight)
    objects = BookingManager()
