from django.test import TestCase
from django.urls import reverse, resolve
from accounts import views

class TestURLs(TestCase):

    def test_home_url_resolves(self):

        assert "/" == reverse("home")
        assert resolve("/").func is views.home

    def test_login_url(self):
        url = reverse("account_login")
        assert url == "/accounts/login/"

    def test_signup_url(self):
        url = reverse("account_signup")
        assert url == "/accounts/signup/"

    def test_logout_url(self):
        url = reverse("account_logout")
        assert url == "/accounts/logout/"

    def test_password_reset_url(self):
        url = reverse("account_reset_password")
        assert url == "/accounts/password/reset/"

    def test_email_verification_sent_url(self):
        url = reverse("account_email_verification_sent")
        assert url == "/accounts/confirm-email/"

    def test_admin_url(self):
        url = reverse("admin:index")
        assert url == "/admin/"