import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProvidersConfig(AppConfig):
    name = "staytrade.providers"
    verbose_name = _("Providers")

    def ready(self):
        with contextlib.suppress(ImportError):
            import staytrade.users.signals  # noqa: F401
