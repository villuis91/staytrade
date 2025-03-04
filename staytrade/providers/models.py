from staytrade.shared.abstract_models import TimeStampedModel, SoftDeletedTimestamped
from staytrade.users.models import User, EnterpriseAccount
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class Hotel(SoftDeletedTimestamped):
    # Relational fields
    created_by = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        verbose_name=_("User that creates hotel."),
        help_text="User that added the hotel.",
        null=False,
        blank=False,
    )
    account = models.ForeignKey(
        EnterpriseAccount,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text=_("Hotel's enterprise."),
        verbose_name=_("Enterprise Account"),
    )

    # Description fields
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
    )
    description = models.TextField(
        verbose_name=_("Hotel's description."), help_text=_("Brief hotel's description")
    )
    stars = models.IntegerField(
        verbose_name=_("Hotel stars"),
        help_text=_("Hotel stars"),
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        null=False,
        blank=False,
    )

    # Urls
    google_maps_location = models.URLField(
        verbose_name=_("Google maps url."),
        null=True,
        blank=True,
    )
    site_url = models.URLField(
        verbose_name=_("Site url."),
        null=True,
        blank=True,
    )

    # Pictures
    # Consider to use a model linked to Rooms with images +Calls but +elegant
    _upload_destine_root = "hotel-pictures/"
    main_picture = models.ImageField(
        _("Main picture."),
        max_length=32,
        blank=True,
        null=True,
        upload_to=_upload_destine_root,
        help_text=_("Hotel's main picture"),
    )
    second_picture = models.ImageField(
        _("Second picture."),
        max_length=32,
        blank=True,
        null=True,
        upload_to=_upload_destine_root,
        help_text=_("Hotel's second picture"),
    )
    third_picture = models.ImageField(
        _("Third picture."),
        max_length=32,
        blank=True,
        null=True,
        upload_to=_upload_destine_root,
        help_text=_("Hotel's third picture"),
    )


class RoomType(SoftDeletedTimestamped):
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
    )
    description = models.TextField()
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.DO_NOTHING,
        null=False,
        blank=False,
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        verbose_name=_("User that creates hotel."),
        help_text=_("User that added the hotel."),
        null=False,
        blank=False,
    )
    # Pictures
    _upload_destine_root = "room-pictures/"
    main_picture = models.ImageField(
        _("Main picture."),
        max_length=32,
        blank=True,
        null=True,
        upload_to=_upload_destine_root,
        help_text=_("Room type's main picture"),
    )
    secondary_picture = models.ImageField(
        _("Second picture."),
        max_length=32,
        blank=True,
        null=True,
        upload_to=_upload_destine_root,
        help_text=_("Room type's second picture"),
    )
    third_picture = models.ImageField(
        _("Second picture."),
        max_length=32,
        blank=True,
        null=True,
        upload_to=_upload_destine_root,
        help_text=_("Room type's third picture"),
    )


class RoomTypeAvailability(TimeStampedModel):
    room_type = models.ForeignKey(
        RoomType,
        on_delete=models.CASCADE,
        related_name="availabilities",
        null=False,
        blank=False,
    )
    start_date = models.DateField(
        null=False,
        blank=False,
    )
    end_date = models.DateField(
        null=False,
        blank=False,
    )

    # Date range intersections must be controlled
    class Meta:
        unique_together = ("room_type", "start_date", "end_date")


class Room(SoftDeletedTimestamped):
    class RoomStatus(models.TextChoices):
        AVAILABLE = "available", _("Available")
        OCCUPIED = "occupied", _("Occupied")

    room_type = models.ForeignKey(
        RoomType,
        on_delete=models.DO_NOTHING,
        null=False,
        blank=False,
    )
    name_or_number = models.CharField(
        max_length=255,
        verbose_name=_("Room name or number."),
        help_text=_("Name or number of the room."),
        null=False,
        blank=False,
    )
    capacity = models.PositiveIntegerField(
        verbose_name=_("Capacity"),
        help_text=_("Maximum number of guests allowed in the room."),
        validators=[MinValueValidator(1)],
    )
    status = models.CharField(
        max_length=15,
        choices=RoomStatus.choices,
        default=RoomStatus.AVAILABLE,
        verbose_name=_("Room status"),
        null=False,
        blank=False,
    )
    internal_notes = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Internal notes"),
        help_text=_("Internal notes for hotel management (not visible to guests)."),
    )


class RoomAvailability(TimeStampedModel):
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name="availabilities"
    )
    start_date = models.DateField(
        null=False,
        blank=False,
    )
    end_date = models.DateField(
        null=False,
        blank=False,
    )
    is_available = models.BooleanField(
        default=True,
        null=False,
        blank=False,
    )

    class Meta:
        unique_together = ("room", "start_date", "end_date")


class RoomNight(SoftDeletedTimestamped):
    entry_datetime = models.DateTimeField(
        null=False,
        blank=False,
    )
    departure_datetime = models.DateTimeField(
        null=False,
        blank=False,
    )
    entry_date = models.DateField(
        null=False,
        blank=False,
    )
    departure_date = models.DateField(
        null=False,
        blank=False,
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.DO_NOTHING,
        null=False,
        blank=False,
    )
