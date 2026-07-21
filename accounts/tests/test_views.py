import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.messages import get_messages


class TestloginView:

    def test_get_authenticated_user_redirects(self, auth_client):
        response = auth_client.get(reverse("account_login"))
        assert response.status_code == 302
        assert response.url == reverse("home")

    
    @pytest.mark.django_db
    def test_login_get_renders_template(self, client: Client):
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


    def test_post_invalid_credentials(self, client: Client, verified_user):
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
