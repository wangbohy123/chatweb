from django.shortcuts import render, redirect
from django.http import *
from client.models import Ordinary_User
from .models import Date


def view_table(request):
    uid = request.session.get('uid', default=None)
    user = Ordinary_User.users.get(id=uid)
    date_tables = user.date.all()
    print(date_tables)
    already = []
    going = []
    for table in date_tables:
        if table.status == False:
            going.append(table)
        else:
            already.append(table)
    context = {
        'uname': user.account_number,
        'tables':date_tables,
        'already':already,
        'going':going,
    }
    return render(request, 'show_date.html', context)

def add_table(request):
    uid = request.session.get('uid', default=None)
    user = Ordinary_User.users.get(id=uid)
    post = request.POST
    task_name = post.get('task_content')
    task_remarks = post.get('task_descr')

    task = Date.tables.create(user=user,
                              thing_name=task_name,
                              remark=task_remarks)
    return redirect('date:show_date')

def change_status(request):
    post = request.POST
    task_id = post.get('task_id')
    task = Date.tables.get(id=task_id)
    task.status = True
    task.save()
    return redirect('date:view_tables')

def view_tables(request):
    uid = request.session.get('uid', default=None)
    user = Ordinary_User.users.get(id=uid)
    date_tables = user.date.all()
    print(date_tables)
    already = []
    going = []
    for table in date_tables:
        if table.status == False:
            going.append(table)
        else:
            already.append(table)
    context = {
        'uname': user.account_number,
        'tables': date_tables,
        'already': already,
        'going': going,
    }
    return render(request, 'view_tables.html', context)

def view_finished(request):
    uid = request.session.get('uid', default=None)
    user = Ordinary_User.users.get(id=uid)
    date_tables = user.date.all()
    print(date_tables)
    already = []
    going = []
    for table in date_tables:
        if table.status == False:
            going.append(table)
        else:
            already.append(table)
    context = {
        'uname': user.account_number,
        'tables': date_tables,
        'already': already,
        'going': going,
    }
    return render(request, 'view_finished.html', context)

def delete_task(request):
    uid = request.session.get('uid', default=None)
    user = Ordinary_User.users.get(id=uid)
    task_id = request.POST.get('task_id')
    task = Date.tables.get(id=task_id)
    task.delete()
    return redirect('date:view_finished')
