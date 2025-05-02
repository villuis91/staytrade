from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ReservationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "staytrade.reservations"
    verbose_name = _("Providers")
