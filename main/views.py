from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from accounts.models import User
import datetime, calendar


@login_required
def index(request):
    return render(request, 'base.html')


def mapping_cal(user, year, month, mode):
    cal = calendar.month(year, month)
    cal = cal.split('\n')

    data = {
        'title': cal[0],
        'year': year,
        'month': month,
    }

    # 스케줄 관리
    if mode == 1:
        weeks = loading_all_plans(year, month, cal)
    # 조회
    elif mode == 2:
        results = loading_individual_logs(user, year, month, cal)
        weeks = results[0]
        data['all_hours'] = results[1]
    # 슈퍼유저 조회
    else:
        results = loading_cal_and_users(user, cal)
        weeks = results[0]
        data['all_users'] = results[1]

    weeks.pop()

    if len(weeks[0]) != 7:
        while len(weeks[0]) < 7:
            weeks[0].insert(0, " ")

    data['weeks'] = weeks

    return data


def loading_individual_logs(user, year, month, cal):
    all_hours = 0
    weeks = []
    for i in range(2, len(cal)):
        line = cal[i]
        dates = line.split()
        days = []
        for day in dates:
            today = datetime.datetime(year=year, month=month, day=int(day))
            logs = Log.objects.filter(date=today, user=user)
            if logs:
                day = {'date': int(day), 'log': logs[0]}
                all_hours += logs[0].hours
            else:
                day = {'date': int(day)}
            days.append(day)

        weeks.append(days)

    return (weeks, all_hours)


def loading_all_plans(year, month, cal):
    weeks = []
    for i in range(2, len(cal)):
        line = cal[i]
        dates = line.split()
        days = []
        for day in dates:
            today = datetime.datetime(year=year, month=month, day=int(day))
            plans = Plan.objects.filter(date=today)
            if plans:
                people = len(plans)
                plan_all = []
                for plan in plans:
                    individual_plan = {
                        'username': str(plan.user.username),
                        'start': plan.start,
                        'end': plan.end
                    }
                    plan_all.append(individual_plan)
                    #한 명의 plan이 dict 형태로 그 dict를 list로 묶음
                day = {'date': int(day), 'plans': plan_all, 'people': people}
            else:
                day = {'date': int(day)}
            days.append(day)

        weeks.append(days)

    return weeks


def loading_cal_and_users(user, cal):
    all_users = User.objects.filter(is_superuser=False)
    weeks = []
    for i in range(2, len(cal)):
        line = cal[i]
        dates = line.split()
        days = []
        for day in dates:
            day = {'date': int(day)}
            days.append(day)

        weeks.append(days)
    return weeks, all_users


end_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def mapping_week(user, year, month, day):
    today = datetime.datetime.now()
    cal = calendar.month(year, month)
    cal = cal.split('\n')
    week = 0
    line = " "
    is_day = 0

    for i in range(2, len(cal)):
        week += 1
        if str(day) in cal[i]:
            line = cal[i]
            break

    data = {
        'title': cal[0],
        'year': year,
        'month': month,
        'week': week
    }

    date_list = list(map(int, line.split()))

    day_list = []
    first_weekday = calendar.weekday(year, month, date_list[0])
    last_weekday = calendar.weekday(year, month, date_list[len(date_list)-1])
    if first_weekday != 0:
        i = 0
        while i != first_weekday:
            day_info = {'date': end_month[month-2]-first_weekday+i+1, 'flag': 1}
            day_list.append(day_info)
            i += 1
    for date in date_list:
        if not is_day:
            data['day'] = date
            is_day = 1
        datetime_obj = datetime.datetime(year=year, month=month, day=date)
        if Plan.objects.filter(date=datetime_obj, user=user):
            plan = Plan.objects.get(date=datetime_obj, user=user)
            day_info = {'date': date, 'form': plan}
        else:
            day_info = {'date': date}
        if datetime_obj.date() == today.date():
            day_info['today'] = 1
        day_list.append(day_info)
    if last_weekday != 6:
        i = last_weekday+1
        while i != 7:
            day_info = {'date': i-last_weekday, 'flag': 1}
            day_list.append(day_info)
            i += 1
    data['all_day'] = day_list

    return data


@login_required
def plan(request):
    user = request.user
    today = datetime.datetime.now()
    if datetime.datetime(year=today.year, month=2, day=29):
        end_month[1] = 29
    if request.method == "POST":
        form = request.POST
        year = int(form['year'])
        month = int(form['month'])
        day = int(form['day'])
        move = form['move']
        if move == "before":
            if month == 1 and day-1 < 7:
                year -= 1
                month = 12
                day = 31
            elif day-1 < 7:
                month -= 1
                day = end_month[month-1]
            else:
                day -= 7
            data = mapping_week(user, year, month, day)
        else:
            if month == 12 and end_month[month-1]-day < 7:
                year += 1
                month = 1
                day = 1
            elif end_month[month-1]-day < 7:
                month += 1
                day = 1
            else:
                day += 7
            data = mapping_week(user, year, month, day)
    else:
        data = mapping_week(user, today.year, today.month, today.day)
    return render(request, 'plan.html', data)


@login_required
def schedule_inquiry(request):
    user = request.user
    today = datetime.datetime.now()
    data = mapping_cal(user, today.year, today.month, 1)
    if request.method == "POST":
        form = request.POST
        year = int(form['year'])
        month = int(form['month'])
        move = form['move']
        if move == "before":
            if month == 1:
                move_datetime = datetime.datetime(year=year - 1, month=12, day=1)
            else:
                move_datetime = datetime.datetime(year=year, month=month - 1, day=1)
            data = mapping_cal(user, move_datetime.year, move_datetime.month, 1)
        else:
            if month == 12:
                move_datetime = datetime.datetime(year=year + 1, month=1, day=1)
            else:
                move_datetime = datetime.datetime(year=year, month=month + 1, day=1)

            data = mapping_cal(user, move_datetime.year, move_datetime.month, 1)
    return render(request, 'schedule_inquiry.html', data)


@login_required
def input(request):
    if request.method == "POST":
        form = CreateLog(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = User.objects.get(username=request.user)
            log.contents = form.cleaned_data['contents'].replace('\r\n', ', ')
            log.save()
            return redirect('look_up')
    else:
        form = CreateLog()
    return render(request, 'input.html', {'form': form})


@login_required
def input_edit(request):
    if request.method == "POST":
        pk = int(request.POST['pk'])
        log = Log.objects.get(pk=pk)
        form = CreateLog(instance=log)
        return render(request, 'input_edit.html', {'form': form, 'pk': pk })


@login_required
def save_input(request, pk):
    log = Log.objects.get(pk=pk)
    if request.method == "POST":
        form = CreateLog(request.POST, instance=log)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = User.objects.get(username=request.user)
            log.save()
            return redirect('look_up')
        return redirect('input_edit')


@login_required
def look_up(request):
    user = request.user
    today = datetime.datetime.now()
    data = mapping_cal(user, today.year, today.month, 2)
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
            data = mapping_cal(user, move_datetime.year, move_datetime.month, 2)
        else:
            if month == 12:
                move_datetime = datetime.datetime(year=year+1, month=1, day=1)
            else:
                move_datetime = datetime.datetime(year=year, month=month+1, day=1)
            data = mapping_cal(user, move_datetime.year, move_datetime.month, 2)

    return render(request, 'look_up.html', data)


@login_required
def look_up_super(request):
    user = request.user
    today = datetime.datetime.now()
    data = mapping_cal(user, today.year, today.month, 3)
    if request.method == "POST":
        form = request.POST
        year = int(form['year'])
        month = int(form['month'])
        move = form['move']
        if move == "before":
            if month == 1:
                move_datetime = datetime.datetime(year=year - 1, month=12, day=1)
            else:
                move_datetime = datetime.datetime(year=year, month=month - 1, day=1)
            data = mapping_cal(user, move_datetime.year, move_datetime.month, 3)
        else:
            if month == 12:
                move_datetime = datetime.datetime(year=year + 1, month=1, day=1)
            else:
                move_datetime = datetime.datetime(year=year, month=month + 1, day=1)
            data = mapping_cal(user, move_datetime.year, move_datetime.month, 3)

    return render(request, 'look_up_super.html', data)


@login_required
def look_up_super_detail(request, username):
    if User.objects.filter(username=username):
        user = User.objects.get(username=username)
        today = datetime.datetime.now()
        data = mapping_cal(user, today.year, today.month, 2)
        if request.method == "POST":
            form = request.POST
            year = int(form['year'])
            month = int(form['month'])
            move = form['move']
            if move == "before":
                if month == 1:
                    move_datetime = datetime.datetime(year=year - 1, month=12, day=1)
                else:
                    move_datetime = datetime.datetime(year=year, month=month - 1, day=1)
                data = mapping_cal(user, move_datetime.year, move_datetime.month, 2)
            else:
                if month == 12:
                    move_datetime = datetime.datetime(year=year + 1, month=1, day=1)
                else:
                    move_datetime = datetime.datetime(year=year, month=month + 1, day=1)
                data = mapping_cal(user, move_datetime.year, move_datetime.month, 2)
        data['username'] = username
        data['all_users'] = User.objects.filter(is_superuser=False)
        return render(request, 'look_up_super.html', data)

    else:
        return False


@login_required
def save_plan(request):
    if request.method == "POST":
        result = dict(request.POST)
        values = list(result.values())
        i = 0
        for value in values:
            if value[0].find('-') != -1:
                break
            i += 1
        values = values[i:]
        values_day = []
        value_day = {}
        for i in range(len(values)):
            if i % 3 == 0:
                if i != 0:
                    values_day.append(value_day)
                    value_day = {}
                value_day['date'] = values[i][0]
            elif i % 3 == 1:
                value_day['start'] = values[i][0]
            else:
                value_day['end'] = values[i][0]
        values_day.append(value_day)
        for value in values_day:
            if 'date' in value and '-' in value['date']:
                if value['start'] != '' and value['end'] != '':
                    user = User.objects.get(username=request.user)
                    if Plan.objects.filter(date=value['date'], user=user):
                        plan = Plan.objects.get(date=value['date'], user=user)
                    else:
                        plan = Plan()
                        plan.date = value['date']
                        plan.user = user
                    plan.start = value['start']
                    plan.end = value['end']
                    plan.save()
    return redirect('schedule_inquiry')