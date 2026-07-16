import pytest
from django.contrib.auth import get_user_model

pytestmark = pytest.mark.django_db

def test_custom_user_str_returns_username_and_age(user):
    assert str(user) == f"Name: {user.username} Age: {user.age}"