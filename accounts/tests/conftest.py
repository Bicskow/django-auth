import pytest
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
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
def social_app(db):
    site = Site.objects.get_current()
    app, _ = SocialApp.objects.get_or_create(
        provider="google",
        defaults={
            "name": "Google",
            "client_id": "test-client-id",
            "secret": "test-secret"
        }
    )
    if site not in app.sites.all():
        app.sites.add(site)
    return app

@pytest.fixture
def auth_client(client, verified_user):
    client.force_login(verified_user)
    return client
    
