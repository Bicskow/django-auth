import pytest
from allauth.account.models import EmailAddress
from .factories import UserFactory


@pytest.fixture
def user(db):
    return UserFactory()

@pytest.fixture
def verified_user(db, user):
    EmailAddress.objects.create(
        user=user,
        email=user.email,
        primary=True,
        verified=True
    )
    return user

@pytest.fixture
def auth_client(client, verified_user):
    client.force_login(verified_user)
    return client
    
