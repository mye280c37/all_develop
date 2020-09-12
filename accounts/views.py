from django.shortcuts import render, redirect
from .forms import *
from .models import *

# Create your views here.
def sign_up(request):
    if request.method == "POST":
        form = CreateAccount(request.POST)
        if form.is_valid():
            form.save()
            return redirect('input')
    else:
        form = CreateAccount()

    return render(request, 'sign_up.html', {'form': form})