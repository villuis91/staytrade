from django.db import models
from .managers import RoomNightManager, BookingManager
from staytrade.shared.abstract_models import SoftDeletedTimestamped
from staytrade.providers.models import RoomType
from staytrade.users.models import User


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
    check_in = models.DateTimeField(
        null=False,
        blank=False,
    )
    check_out = models.DateTimeField(
        null=False,
        blank=False,
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pendiente"),
            ("confirmed", "Confirmada"),
            ("cancelled", "Cancelada"),
        ],
        default="pending",
    )
    room_nights = models.ManyToManyField(RoomNight)
    objects = BookingManager()
