import pytest
from allauth.account.models import EmailAddress
from .factories import UserFactory

@pytest.fixture
def user(db):
    return UserFactory()