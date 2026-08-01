import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

pytestmark = pytest.mark.django_db
CustomUser = get_user_model()

class TestCustomUserModel:

    def test_custom_user_str_returns_username_and_age(self, user):
        assert str(user) == f"Name: {user.username} Age: {user.age}"


    def test_create_user(self):
        usr = CustomUser.objects.create_user(
            email = "test@example.com",
            username = "username",
            password = "12345",
            first_name = "Jane",
            last_name = "Doe",
            age = 30,
            country = "PL"
        )

        assert usr.email == "test@example.com"
        assert usr.username == "username"
        assert usr.check_password("12345")
        assert usr.first_name == "Jane"
        assert usr.last_name == "Doe"
        assert usr.age == 30
        assert usr.country == "PL"
        assert usr.is_active is True
        assert usr.is_staff is False
        assert usr.is_superuser is False


    def test_create_user_wo_optional_values(self):
        usr = CustomUser.objects.create_user(
            email = "test@example.com",
            username="test@example.com"
        )
        assert usr.email == "test@example.com"
        assert usr.username == "test@example.com"
        assert usr.first_name == ""
        assert usr.last_name == ""
        assert usr.age is None
        assert usr.country == ""
        assert usr.is_active is True
        assert usr.is_staff is False
        assert usr.is_superuser is False


    def test_create_user_wo_required_argument(self):
        with pytest.raises(TypeError):
            CustomUser.objects.create_user(
                email = "test@example.com"
            )


    def test_user_inherits_from_abstract_user(self, user):
        assert isinstance(user, AbstractUser)

    def test_usermodel_settings(self):
        assert settings.AUTH_USER_MODEL == "accounts.CustomUser"
