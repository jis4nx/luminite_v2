from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model


class Luminite_UserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("email",)


class Luminite_UserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ("email",)
