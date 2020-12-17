from django.shortcuts import render, redirect
from .models import Massage
from client.models import Ordinary_User
from client.views import get
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

@csrf_exempt
def get_massage(request):
    uid = request.session.get('uid', default=None)
    user = Ordinary_User.users.get(id=uid)
    friends = get(request)
    id_list = []
    friends_list = []
    if friends['msg'] == 'OK':
        for item in friends['data']:
            id_list.append(item['friend_id'])

    for i in id_list:
        u = Ordinary_User.users.get(id=i)
        friends_list.append(u.account_number)

    context = {
        'uname': user.account_number,
        'friends': friends,
        'account_number': friends_list,
        'count': len(friends_list)
    }

    post = request.POST
    friend_number = post.get('friend')
    friend = Ordinary_User.users.get(account_number=friend_number)

    # 获得当前用户作为接收者收到的信息
    massages_from_friend = Massage.massages.filter(sender=friend)
    print(massages_from_friend)

    return redirect('user:index_for_user')

def show_room(request):
    friend = request.GET.get('friend')
    uid = request.session.get('uid', default=None)
    user = Ordinary_User.users.get(id=uid)

    massages = Massage.massages.filter(
        Q(sender__id=uid, receiver__account_number=friend) |
        Q(sender__account_number=friend, receiver__id=uid))

    # friend_id = Ordinary_User.users.get(account_number=friend).id
    # [<Massage: test>, <Massage: test02>]

    objs = []
    if_sender = []
    for m in massages:
        objs.append(m)

    f_obj = Ordinary_User.users.get(account_number=friend)

    context = {
        'uname': user.account_number,
        'friend_number':friend,
        'massages':objs,
        'uid':uid,
        # 'fid':friend_id,
        'friend':f_obj,
    }
    return render(request, 'chat_room.html', context)

def send_massage(request):
    if request.method == 'POST':
        post = request.POST
        massage = post.get('data')
        sender_number = post.get('from')
        receiver_number = post.get('to')

        sender = Ordinary_User.users.get(account_number=sender_number)
        receiver = Ordinary_User.users.get(account_number=receiver_number)

        Massage.massages.create(sender, receiver, massage)
        return redirect('/chat/show_room?friend=' + str(receiver_number))