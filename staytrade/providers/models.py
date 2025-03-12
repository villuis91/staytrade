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
        help_text=_("This will be the public hotel's name."),
        verbose_name=_("Hotel's name"),
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
        help_text=_("Google maps location link"),
        null=True,
        blank=True,
    )
    site_url = models.URLField(
        verbose_name=_("Site url."),
        help_text=_("Your allocation website."),
        null=True,
        blank=True,
    )
    contact_phone = models.PositiveIntegerField(
        verbose_name="Contact phone number",
        help_text="Hotel's phone number.",
        null=True,
    )
    text_location = models.CharField(
        verbose_name=_("Location"),
        help_text=_("The public location text"),
        max_length=255,
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

    class Meta:
        unique_together = ("created_by", "name")


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
    adults_capacity = models.PositiveIntegerField(
        verbose_name=_("Adults Capacity"),
        help_text=_("Maximum number of adult guests allowed in the room."),
        validators=[MinValueValidator(1)],
        default=2,
    )
    children_capacity = models.PositiveIntegerField(
        verbose_name=_("Children Capacity"),
        help_text=_("Maximum number of children guests allowed in the room."),
        validators=[MinValueValidator(1)],
        default=1,
    )
    stock = models.IntegerField(
        verbose_name=_("Number of rooms"),
        help_text=_("Number of rooms of the given room type."),
        validators=[MinValueValidator(1)],
        null=False,
        blank=False,
        default=1,
    )
    is_available = models.BooleanField(
        verbose_name=_("Is available"),
        help_text=_("Determines if the room type is available to be sold."),
        blank=False,
        null=False,
        default=False,
    )
    internal_notes = models.TextField(
        blank=True,
        verbose_name=_("Internal notes"),
        help_text=_("Internal notes for hotel management (not visible to guests)."),
    )

    # Date range intersections must be controlled
    class Meta:
        unique_together = ("hotel", "name")


class RoomTypeAvailability(TimeStampedModel):
    room_type = models.ForeignKey(
        RoomType,
        on_delete=models.CASCADE,
        related_name="availabilities",
        null=False,
        blank=False,
    )
    start_date = models.DateField(
        verbose_name=_("Initial date"),
        help_text=_("Initial date of disponibility period."),
        null=False,
        blank=False,
    )
    end_date = models.DateField(
        verbose_name=_("Final date"),
        help_text=_("Final date of disponibility period."),
        null=False,
        blank=False,
    )

    # Date range intersections must be controlled
    class Meta:
        unique_together = ("room_type", "start_date", "end_date")


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
    room_type = models.ForeignKey(
        RoomType,
        on_delete=models.DO_NOTHING,
        null=False,
        blank=False,
    )
