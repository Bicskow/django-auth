import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth import get_user_model
from django.conf import settings


CustomUser = get_user_model()

class TestloginView:

    def test_get_authenticated_user_redirects(self, auth_client):
        response = auth_client.get(reverse("account_login"))
        assert response.status_code == 302
        assert response.url == reverse("home")

    
    @pytest.mark.django_db
    def test_login_get_renders_template(self, client: Client, social_app):
        response = client.get(reverse("account_login"))
        assert response.status_code == 200
        assert response.templates[0].name == "account/login.html"


    def test_post_valid_credentials(self, client: Client, verified_user):
        response = client.post(reverse("account_login"),
                    {
                        "login": verified_user.email,
                        "password": "strongpass123!"
                    })
        
        assert response.status_code == 302
        assert response.url == reverse("home")
        assert response.wsgi_request.user.is_authenticated


    def test_post_invalid_credentials(self, client: Client, verified_user, social_app):
        response = client.post(reverse("account_login"),
                    {
                        "login": verified_user.email,
                        "password": "wrongpass!"
                    })

        assert response.status_code == 200
        assert not response.wsgi_request.user.is_authenticated

    
    def test_login_requires_email_verification(self, client: Client, user):
        response = client.post(reverse("account_login"),
                    {
                        "login": user.email,
                        "password": "strongpass123!"
                    })

        assert response.status_code == 302
        assert response.url == reverse("account_email_verification_sent")
        assert not response.wsgi_request.user.is_authenticated
        messages = list(get_messages(response.wsgi_request))
        assert any("Confirmation email sent" in str(m) for m in messages)


class TestHomeView:

    def test_requires_login(self, client):
        response = client.get(reverse("home"))

        assert response.status_code == 302
        assert reverse("account_login") in response.url


    def test_authenticated_user_sees_home(self, auth_client):
        response = auth_client.get(reverse("home"))

        assert response.status_code == 200
        assert response.templates[0].name == "home.html"


class TestLogoutView:

    def test_post_logs_out(self, auth_client):
        response = auth_client.post(reverse("account_logout"))

        assert response.status_code == 302
        assert response.url == reverse("account_login")
        assert not response.wsgi_request.user.is_authenticated


    def test_requires_login(self, client):
        response = client.post(reverse("account_logout"))
        
        assert response.status_code == 302
        assert reverse("account_login") in response.url

    
    def test_logout_sets_info_message(self, auth_client, social_app):
        response = auth_client.post(reverse("account_logout"), follow=True)

        messages = list(get_messages(response.wsgi_request))

        assert response.status_code == 200
        assert any("logged out" in str(m).lower() for m in messages)


class TestRegistrationView:

    @pytest.mark.django_db
    def test_registration_get_renders_form(self, client):
        response = client.get(reverse("account_signup"))

        assert response.status_code == 200
        assert "signup" in response.templates[0].name
        assert "form" in response.context


    @pytest.mark.django_db
    def test_post_valid_data(self, client, mailoutbox):
        # Force the in-memory backend so we can inspect the outbox.
        settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

        response = client.post(reverse("account_signup"),
                                data={
                                    'email': 'newuser@example.com',
                                    'first_name': 'New',
                                    'last_name': 'User',
                                    'age': 33,
                                    'country': 'Hungary',
                                    'password1': 'k1k1k1k1',
                                    'password2': 'k1k1k1k1'
                                }
                               )

        assert response.status_code == 302
        assert response.url == reverse("account_email_verification_sent")
        assert CustomUser.objects.filter(email="newuser@example.com").exists()
        assert len(mailoutbox) == 1


    @pytest.mark.django_db
    def test_post_invalid_data(self, client):
        response = client.post(reverse("account_signup"),
                        data={
                            'email': 'newuser@example.com',
                            'first_name': 'New',
                            'last_name': 'User',
                            'age': 33,
                            'country': 'Hungary',
                            'password1': 'k1k1k1k1',
                            'password2': 'wrongpass'
                        }
                        )
        assert response.status_code == 200
        assert 'form' in response.context
        assert response.context['form'].errors
        assert not CustomUser.objects.filter(email="newuser@example.com").exists()



