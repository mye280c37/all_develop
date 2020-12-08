from .models import *
from django.contrib.auth.forms import UserCreationForm


class CreateAccount(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "phone", "password1", "password2"]