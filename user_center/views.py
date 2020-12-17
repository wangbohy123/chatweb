from django.shortcuts import render
from django.http import *
from client.models import Ordinary_User
from client.views import get
# Create your views here.

def show(request):
    uid = request.session.get('uid', default=None)
    user = Ordinary_User.users.get(id=uid)

    friends = get(request)
    id_list = []
    friends_list = []
    mail_list = []
    obj_list = []

    if friends['msg'] == 'OK':
        for item in friends['data']:
            id_list.append(item['friend_id'])

    for i in id_list:
        u = Ordinary_User.users.get(id=i)
        friends_list.append(u.account_number)
        mail_list.append(u.account_mail)
        obj_list.append(u)


    context = {
        'uname': user.account_number,
        'friends': friends,
        'account_number': friends_list,
        'mails':mail_list,
        'count': len(friends_list),
        'objs':obj_list,
    }

    return render(request, 'user_center.html', context)

