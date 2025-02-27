from staytrade.users.models import User
import pytest


@pytest.mark.django_db
def test_create_user_with_default_account_type():
    user = User.objects.create_user(username="trader1", password="test123")
    assert user.account_type == User.AccountTypes.TRADER and user.is_trader()


@pytest.mark.django_db
def test_create_provider_user():
    user = User.objects.create_user(
        username="provider1",
        password="test123",
        account_type=User.AccountTypes.PROVIDER,
    )
    assert user.account_type == User.AccountTypes.PROVIDER and user.is_provider()


@pytest.mark.django_db
def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/users/{user.username}/"
