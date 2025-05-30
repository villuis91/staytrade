from staytrade.shared.abstract_models import SoftDeletedTimestamped
from staytrade.users.models import User, EnterpriseAccount
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from .managers import RoomPriceManager


class Localities(models.Model):
    region = models.CharField(
        max_length=255, verbose_name=_("Region"), help_text=_("Name of region or area")
    )
    province = models.CharField(
        max_length=255, verbose_name=_("Province"), help_text=_("Locations province")
    )
    name = models.TextField(
        max_length=255, verbose_name=_("Name"), help_text=_("Locality Name")
    )
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        unique_together = ("name", "province")


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
    locality = models.ForeignKey(
        Localities, null=True, blank=True, on_delete=models.DO_NOTHING
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
        validators=[MinValueValidator(0)],
        default=1,
    )
    amount = models.IntegerField(
        verbose_name=_("Amount"),
        help_text=_("Amount of rooms of the given room type."),
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


class MealPlan(models.Model):
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    name = models.CharField(
        verbose_name=_("Meal plan name"), help_text=_("Meal plan name"), max_length=255
    )
    details = models.TextField(
        verbose_name=_("Meal plan detail"), help_text=_("Details and meal description")
    )

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("hotel", "name")


class RoomTypeMealPlan(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("room_type", "meal_plan")

    def __str__(self):
        return f"{self.room_type.name} - {self.meal_plan.name}"


class RoomTypeMealPlanPrice(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE)
    start_date = models.DateField(
        verbose_name=_("Start Date"), help_text=_("Start date for this price")
    )
    end_date = models.DateField(
        verbose_name=_("End Date"), help_text=_("End date for this price")
    )
    price = models.DecimalField(
        verbose_name=_("Price"),
        help_text=_("Price for the date range"),
        max_digits=10,
        decimal_places=2,
    )

    objects = RoomPriceManager()

    class Meta:
        unique_together = ("room_type", "meal_plan", "start_date", "end_date")
        # Valdemos rango
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date__gte=models.F("start_date")),
                name="valid_date_range",
            )
        ]

    def __str__(self):
        return f"{self.room_type.name} - {self.meal_plan.name} ({self.start_date} to {self.end_date}): {self.price}€"
