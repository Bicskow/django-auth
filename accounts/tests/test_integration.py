import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress


User = get_user_model()

pytestmark = pytest.mark.django_db

class TestRegistrationAndLoginFlow:

    @pytest.mark.django_db
    def test_full_registration_to_login(self, client, mailoutbox):
        # Step 1: Register
        response = client.post(
            reverse("account_signup"),
            {
                "email": "newuser@example.com",
                "first_name": "New",
                "last_name": "User",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            })

        assert response.status_code == 302
        assert response.url == reverse("account_email_verification_sent")

        # Step 2: User exists in DB but email is unverified
        user = User.objects.get(email="newuser@example.com")
        email_obj = EmailAddress.objects.get(user=user)

        assert email_obj is not None
        assert not email_obj.verified

        # Step 3: Extract confirmation key from email
        assert len(mailoutbox) == 1
        email_body = mailoutbox[0].body


        # Step 4: Confirm email
        import re
        match = re.search(r"/accounts/confirm-email/([^/]+)/", email_body)
        assert match, "Confirmation link not found in email"
        key = match.group(1)


        response = client.post(reverse("account_confirm_email", args=[key]))
        assert response.status_code == 302


        # Step 5: Verify email is now confirmed
        email_obj.refresh_from_db()
        assert email_obj.verified


        # Step 6: Login with credentials
        response = client.post(reverse("account_login"), {
            "login": "newuser@example.com",
            "password": "StrongPass123!",
        })
        assert response.status_code == 302
        assert response.url == reverse("home")
        assert response.wsgi_request.user.is_authenticated


    def test_logout_after_login(self, client, db):
        """Test login then logout flow."""
        # Create and verify user
        user = User.objects.create_user(
            username='logout@example.com',
            email='logout@example.com',
            password='TestPass123!',
        )
        EmailAddress.objects.create(
            user=user,
            email=user.email,
            verified=True,
            primary=True
        )

        # Login
        client.post(reverse('account_login'), {
            'login': 'logout@example.com',
            'password': 'TestPass123!',
        })

        # Verify we can access home
        response = client.get(reverse('home'))
        assert response.status_code == 200

        # Logout
        response = client.post(reverse('account_logout'))
        assert response.status_code == 302

        # Verify we can no longer access home
        response = client.get(reverse('home'))
        assert response.status_code == 302