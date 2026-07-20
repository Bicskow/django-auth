import pytest
from django.urls import reverse

class TestloginView:

    def test_get_authenticated_user_redirects(sefl, auth_client):
        response = auth_client.get(reverse("account_login"))
        assert response.status_code == 302
        assert response.url == reverse("home")