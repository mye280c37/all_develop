from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from accounts.models import User
from schedule import *
import datetime, calendar


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


def mapping_cal(user, year, month):
    cal = calendar.month(year, month)
    cal = cal.split('\n')
    weeks = []
    for i in range(2, len(cal)):
        line = cal[i]
        dates = line.split()
        days = []
        for day in dates:
            today = datetime.datetime(year=year, month=month, day=int(day))
            logs = Log.objects.filter(date=today, user=user)
            day = {'date': int(day), 'logs': logs}
            days.append(day)
        weeks.append(days)

    weeks.pop()

    if len(weeks[0]) != 7:
        print(type(weeks[0]))
        while len(weeks[0]) < 7:
            weeks[0].insert(0, " ")

    data = {
        'weeks': weeks,
        'title': cal[0],
        'year': year,
        'month': month
    }

    print(data)
    return data


def look_up(request):
    user = request.user
    today = datetime.datetime.now()
    data = mapping_cal(user, today.year, today.month)
    if request.method == "POST":
        form = request.POST
        year = int(form['year'])
        month = int(form['month'])
        move = form['move']
        if move == "before":
            if month == 1:
                move_datetime = datetime.datetime(year=year-1, month=12, day=1)
            else:
                move_datetime = datetime.datetime(year=year, month=month-1, day=1)
            data = mapping_cal(user, move_datetime.year, move_datetime.month)
        else:
            if month == 12:
                move_datetime = datetime.datetime(year=year+1, month=1, day=1)
            else:
                move_datetime = datetime.datetime(year=year, month=month+1, day=1)

            data = mapping_cal(user, move_datetime.year, move_datetime.month)

    return render(request, 'look_up.html', data)

