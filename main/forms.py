from django import forms
from .models import *
from django.utils import timezone


class CreateLog(forms.ModelForm):
    date = forms.DateField(initial=timezone.now)
    start = forms.CharField(initial="00:00")
    end = forms.CharField(initial="00:00")
    hours = forms.IntegerField(initial=0)

    class Meta:
        model = Log
        fields = ['date', 'hours', 'contents', 'start', 'end']


class CreatePlan(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['start', 'end']

