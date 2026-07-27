import pytest
from accounts.forms import CustomSignupForm
from django.contrib.auth import get_user_model


class TestCustomSignupForm:

    def test_form_valid_with_required_data(self, db):
        form = CustomSignupForm(
            data={
                "email": "sarah@example.com",
                "first_name": "Sarah",
                "last_name": "Connor",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            }
        )

        assert form.is_valid()


    def test_form_valid_with_optional_fields(self, db):
        form = CustomSignupForm(
            data={
                "email": "sarah@example.com",
                "first_name": "Sarah",
                "last_name": "Connor",
                "age": 30,
                "country": "USA",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            }
        )

        assert form.is_valid()

    def test_form_invalid_with_missing_required_fields(self, db):
        form = CustomSignupForm(
            data={
                "first_name": "Sarah",
                "last_name": "Connor",
                "age": 30,
                "country": "USA",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            }
        )

        assert not form.is_valid()
        assert "email" in form.errors

    def test_form_invalid_with_mismatched_passwords(self, db):
        form = CustomSignupForm(
            data={
                "email": "sarah@example.com",
                "first_name": "Sarah",
                "last_name": "Connor",
                "age": 30,
                "country": "USA",
                "password1": "StrongPass!",
                "password2": "StrongPass123!",
            }
        )

        assert not form.is_valid()
        assert "password2" in form.errors


    def test_save_creates_user_with_correct_attributes(self,db, client):
        form = CustomSignupForm(
            data={
                "email": "sarah@example.com",
                "first_name": "Sarah",
                "last_name": "Connor",
                "age": 30,
                "country": "USA",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            }
        )

        assert form.is_valid()

        response = client.get('/accounts/signup/')
        user = form.save(request=response.wsgi_request)

        assert user.username == "sarah@example.com"
        assert user.first_name == "Sarah"
        assert user.last_name == "Connor"
        assert user.age == 30
        assert user.country == "USA"
        assert user.check_password("StrongPass123!")


    def test_password_help_text_is_empty(self, db):
        form = CustomSignupForm()
        assert form.fields["password1"].help_text == ""
        assert form.fields["password2"].help_text == ""


    @pytest.mark.django_db
    def test_form_requires_first_and_last_name(self):
        data = {
                "email": "jane@example.com",
                "first_name": "",
                "last_name": "",
                "age": 28,
                "country": "Poland",
                "password1": "Str0ng!Pass1",
                "password2": "Str0ng!Pass1"
                 }
        form = CustomSignupForm(data)
        assert not form.is_valid()
        assert "first_name" in form.errors
        assert "last_name" in form.errors


