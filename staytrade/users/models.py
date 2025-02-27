from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, TextChoices
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for Staytrade.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    class AccountTypes(TextChoices):
        PROVIDER = "provider", _("Provider")
        TRADER = "trader", _("Trader")

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    account_type = CharField(
        _("Account Type"),
        max_length=16,
        choices=AccountTypes.choices,
        default=AccountTypes.TRADER,
    )

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
