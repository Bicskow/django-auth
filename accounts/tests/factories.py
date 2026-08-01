import factory
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser
        skip_postgeneration_save = True

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    username = factory.SelfAttribute("email")
    first_name = "Jane"
    last_name = "Doe"
    age = 30
    country = "PL"

    @factory.post_generation
    def password(obj, create, extracted, **kwargs):  # noqa: N805
        obj.set_password(extracted or "strongpass123!")
        if create:
            obj.save()
