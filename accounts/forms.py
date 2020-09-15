from django import forms
from .models import *


class CreateAccount(forms.ModelForm):
    phone = forms.CharField(widget=forms.TextInput(attrs={'type': 'tel', 'pattern': "[0-9]{3}[0-9]{4}[0-9]{4}"}))
    password = forms.CharField(widget=forms.TextInput(attrs={'type': 'password'}))
    class Meta:
        model = User

        fields = ['username', 'email', 'phone', 'password']