from django import forms
from .models import *

class CreateLog(forms.ModelForm):
    date = forms.CharField(widget=forms.TextInput(attrs={'type':'date'}))
    start = forms.CharField(widget=forms.TextInput(attrs={'type': 'time'}))
    end = forms.CharField(widget=forms.TextInput(attrs={'type': 'time'}))
    class Meta:
        model = Log

        fields = ['date', 'hours', 'contents', 'start', 'end']

