from django import forms
from .models import *


class CreateAccount(forms.ModelForm):
    class Meta:
        model = User

        fields = ['username', 'email', 'phone']