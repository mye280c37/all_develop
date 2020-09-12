from django import forms
from .models import *

class CreateLog(forms.ModelForm):
    date = forms.CharField(widget=forms.TextInput(attrs={'type':'date'}))
    class Meta:
        model = Log

        fields = ['date', 'hours', 'contents']