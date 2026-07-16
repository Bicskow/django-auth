import factory
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    username = factory.SelfAttribute("email")
    first_name = "Jane"
    last_name = "Doe"
    age = 30
    country = "PL"