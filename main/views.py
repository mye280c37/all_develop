from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from accounts.models import User


def index(request):
    return render(request, 'base.html')


def input(request):
    if request.method == "POST":
        form = CreateLog(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = User.objects.get(username=request.user)
            log.save()
            print(request.user)
            return redirect('input')
    else:
        form = CreateLog()
    return render(request, 'input.html', {'form': form})


def look_up(request):
    return render(request, 'look_up.html')
