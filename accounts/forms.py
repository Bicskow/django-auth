from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

user = get_user_model()

class RegisterForm(UserCreationForm):
    class Meta:
        model = user
        fields = ["username", "first_name", "last_name", "email", "age", "country", "password1", "password2"]


        help_texts = {
            "username": "",
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""