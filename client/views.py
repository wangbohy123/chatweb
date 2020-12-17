from django.shortcuts import render, redirect
from django.http import request, HttpResponse, HttpResponseNotAllowed
from .models import Ordinary_User, Relationship
from . import serializer # 对象序列化
from collections import OrderedDict
from django.db.models import Q # Q对象表示数据库中进行或的关系的查询


def index(request):
    # 主页的请求
    if request.session.get('uid', default='') == '':
        return render(request, 'index.html')
    else:
        return redirect('/user/index_for_user/')

def login(request):
    # 登陆页面的响应
    buf = verifycode(request)
    image = buf.getvalue()
    context = {
        'image': image,
    }
    return render(request, 'login.html', context)

def register(request):
    # 注册页面的响应
    buf = verifycode(request)
    image = buf.getvalue()
    context = {
        'image': image,
    }
    return render(request, 'register.html')

def login_handel(request):
    # 登录会话 将用户id写入会话里，方便每次提取
    from hashlib import sha1
    post = request.POST
    uname = post.get('uname')
    upwd = post.get('upwd')
    user_kind= post.get('user_kind')
    # code = post.get('verifycode')
    # verifycode = request.session['verifycode']
    s1 = sha1()
    s1.update(upwd.encode('utf-8'))
    pwd = s1.hexdigest()
    # if code != verifycode:
    #     return HttpResponse('验证码错误')

    user = Ordinary_User.users.filter(account_number=uname)
    if len(user) == 1:
        try:
            temp = Ordinary_User.users.get(account_number=uname, account_passWord=pwd)
            print(temp.account_number)
            id = temp.id
            print(id)
        except:
            return HttpResponse('密码错误')
    else:
        return redirect('/user/login/')

    # else:
    #     return HttpResponse('请输入用户种类')

    request.session['uid'] = id
    request.session['user_kind'] = user_kind
    return redirect('/user/index_for_user/')

def register_handel(request):
    # 注册
    from hashlib import sha1

    avatar = request.FILES.get('avatar')

    post = request.POST
    uname = post.get('uname')
    upwd = post.get('upwd')
    cpwd = post.get('cpwd')
    mail = post.get('email', default='123@qq.com')
    nickname = post.get('nickname')
    true_name = post.get('true_name')
    birth = post.get('birth')
    tel = post.get('tel')
    gender = post.get('gender')

    if upwd != cpwd:
        return redirect('/user/register/')

    s1 = sha1()
    s1.update(upwd.encode('utf-8'))
    pwd = s1.hexdigest()

    if Ordinary_User.users.if_has(uname):
        return HttpResponse('repeated')
    # 创建一个用户
    o_user = Ordinary_User.users.create(accountnum=uname,
                                        password=pwd,
                                        mail=mail,
                                        nickname=nickname,
                                        true_name=true_name,
                                        birth=birth,
                                        tel=tel,
                                        gender=gender,
                                        image=avatar)
    # 返回重定向 用户的主页
    return redirect('/user/index/')

def del_session(request):
    # 清除会话的功能 登出功能
    request.session.flush()
    return redirect('/user/index/')


def verifycode(request):
    # 生成验证码的函数
    from PIL import Image, ImageDraw, ImageFont
    import random
    bgcolor = (random.randrange(20, 100), random.randrange(20, 100), 255)
    width = 100
    height = 25
    im = Image.new('RGB', (width, height), bgcolor)
    draw = ImageDraw.Draw(im)
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    font = ImageFont.truetype("Dengb.ttf", 16)
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    del draw
    request.session['verifycode'] = rand_str
    from io import StringIO,BytesIO
    buf = BytesIO()
    im.save(buf, 'png')
    return HttpResponse(buf.getvalue(), 'image/png')

def index_for_user(request):

    uid = request.session.get('uid', default=None)
    user = Ordinary_User.users.get(id=uid)
    # avatar = Avatar.objects.get(user__id=uid)
    # image = avatar.image
    friends = get(request)
    id_list = []
    friends_list = []
    f_list = []
    if friends['msg'] == 'OK':
        for item in friends['data']:
            id_list.append(item['friend_id'])

    for i in id_list:
        u = Ordinary_User.users.get(id=i)
        friends_list.append(u.account_number)
        f_list.append(u)

    context = {
        'uname': user.account_number,
        'friends':friends,
        'account_number':friends_list,
        'count':len(friends_list),
        'avatar':user.avatar,
        'f':f_list,
    }
    return render(request, 'index_for_user.html',context)

def get(request):
    """
    好友序列化
    聊天-好友列表
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    try:
        # chat_id  就是当前登陆的用户id
        chat_id = request.session.get('uid', default=None)
        # chat_id = request.user.user.chat_id  # 添加用户认证后再使用request.user
        chat_user = Ordinary_User.users.get(id=int(chat_id))
    except ValueError:
        return HttpResponse(dict(msg="请输入用户id"))
    except Ordinary_User.DoesNotExist:
        return HttpResponse(dict(msg="用户不存在"))

    # 好友列表
    user_friends = Relationship.relate.filter(Q(user_id=chat_id, if_pass=True) |
                                              Q(friend_id=chat_id, if_pass=True))

    ser = serializer.FriendSerializer(instance=user_friends,
                                      many=True,
                                      context={
                                          "chat_user": chat_user
                                      })

    friends = []
    for data in ser.data:
        friend_dict = OrderedDict()
        if data["user_id"] == int(chat_id):
            friend_dict["friend_id"] = data["friend_id"]
            # friend_dict["friend_avatar"] = data["friend_avatar"]
        if data["friend_id"] == int(chat_id):
            friend_dict["friend_id"] = data["user_id"]
            # friend_dict["friend_avatar"] = data["user_avatar"]
        # friend_dict["friend_name"] = data["friend_name"]
        # friend_dict["friend_area"] = data["friend_area"]
        # friend_dict["friend_status"] = data["friend_status"]
        friend_dict["friend_label"] = data["friend_label"]
        # friend_dict["friend_resource"] = data["friend_resource"]
        friends.append(friend_dict)
    # logger.debug("data:%s", ser.data)

    return dict(msg="OK", data=friends)
    # return friends

def friends_config(request):
    if_research = False
    uid = request.session.get('uid', default=None)
    user = Ordinary_User.users.get(id=uid)
    friends = get(request)
    # avatar = Avatar.objects.get(user__id=uid)
    # image = avatar.image
    id_list = []
    friends_list = []
    f_list = []
    if friends['msg'] == 'OK':
        for item in friends['data']:
            id_list.append(item['friend_id'])

    for i in id_list:
        u = Ordinary_User.users.get(id=i)
        friends_list.append(u.account_number)
        f_list.append(u)

    context = {
        'uname': user.account_number,
        'friends': friends,
        'account_number': friends_list,
        'count': len(friends_list),
        'if_research':if_research,
        'avatar': user.avatar,
        'f':f_list,
    }

    if request.method == 'POST':
        # 朋友的查找
        available = True
        post = request.POST
        search_id = post.get('research')
        try:
            user = Ordinary_User.users.get(account_number=search_id)
        except:
            massage = '没有这个人！'
            context = {
                'uname': user.account_number,
                'friends': friends,
                'account_number': friends_list,
                'count': len(friends_list),
                'if_research': True,
                'massage':massage,
                'available':available,
                'avatar': user.avatar,
                'f': f_list,
            }
            return render(request, 'friends_config.html', context)
        massage = user.account_number
        available = False
        context = {
            'uname': user.account_number,
            'friends': friends,
            'account_number': friends_list,
            'count': len(friends_list),
            'if_research': True,
            'available':available,
            'massage': massage,
            'avatar': user.avatar,
        }

    return render(request, 'friends_config.html', context)

def view_friend(request):
    # 查看朋友信息
    uid = request.session.get('uid', default=None)
    user = Ordinary_User.users.get(id=uid)
    # avatar = Avatar.objects.get(user__id=uid)
    # image = avatar.image
    friends = get(request)
    id_list = []
    friends_list = []
    f_list = []
    if friends['msg'] == 'OK':
        for item in friends['data']:
            id_list.append(item['friend_id'])

    for i in id_list:
        u = Ordinary_User.users.get(id=i)
        friends_list.append(u.account_number)
        f_list.append(u)
    if request.method == 'POST':
        # 朋友信息
        post = request.POST
        id = post.get('friendID')
        friend = Ordinary_User.users.get(account_number=id)
        number = friend.account_number
        mail = friend.account_mail
        nickname = friend.nickname

        context = {
            'uname': user.account_number,
            'friends': friends,
            'account_number': friends_list,
            'count': len(friends_list),
            'avatar':user.avatar,
            'f':f_list,
            'number':number,
            'mail':mail,
            'nickname':nickname,
            'friend':friend,
        }

        return render(request, 'show_friend.html', context)

    else:
        return HttpResponseNotAllowed

def add_page(request):
    uid = request.session.get('uid', default=None)
    user = Ordinary_User.users.get(id=uid)
    friends = get(request)
    id_list = []
    friends_list = []
    f_list = []
    if friends['msg'] == 'OK':
        for item in friends['data']:
            id_list.append(item['friend_id'])

    for i in id_list:
        u = Ordinary_User.users.get(id=i)
        friends_list.append(u.account_number)
        f_list.append(u)
    context = {
        'uname': user.account_number,
        'friends': friends,
        'account_number': friends_list,
        'count': len(friends_list),
        'avatar': user.avatar,
        'f':f_list,
    }

    if request.method == 'POST':
        # 朋友的查找
        available = True
        post = request.POST
        search_id = post.get('research')
        try:
            user_for_find = Ordinary_User.users.get(account_number=search_id)
        except:
            massage = '没有这个人！'
            context = {
                'uname': user.account_number,
                'friends': friends,
                'account_number': friends_list,
                'count': len(friends_list),
                'if_research': True,
                'massage':massage,
                'available':available,
                'avatar': user.avatar,
                'f': f_list,
            }
            return render(request, 'add_page.html', context)
        massage = user_for_find.account_number
        available = False
        context = {
            'uname': user.account_number,
            'friends': friends,
            'account_number': friends_list,
            'count': len(friends_list),
            'if_research': True,
            'available':available,
            'massage': massage,
            'avatar': user.avatar,
            'f': f_list,
        }

    return render(request, 'add_page.html', context)

def add_friend(request):
    # 添加朋友
    uid = request.session.get('uid', default=None)
    user = Ordinary_User.users.get(id=uid)
    print(user)
    post = request.POST
    number = post.get('number')
    print(number)
    try:
        friend = Ordinary_User.users.get(account_number=number)
    except:
        return redirect('/user/add_page/')
    print(friend)
    print(friend.id)
    # try:
    relation = Relationship.relate.create(user, friend)
    print(relation)
    # except:
    #     # 如果没有添加成功 返回错误
    #     return HttpResponseForbidden

    return redirect('/user/add_page/')

def find_friend(request):
    # 查找可能认识的人
    uid = request.session.get('uid', default=None)
    user = Ordinary_User.users.get(id=uid)
    possible = {}

    friends = get(request)
    id_list = []
    friends_list = []
    f_list = []
    if friends['msg'] == 'OK':
        for item in friends['data']:
            id_list.append(item['friend_id'])

    for i in id_list:
        u = Ordinary_User.users.get(id=i)
        friends_list.append(u.account_number)
        f_list.append(u)

    context = {
        'uname': user.account_number,
        'friends': friends,
        'account_number': friends_list,
        'count': len(friends_list),
        'avatar':user.avatar,
        'f':f_list,
    }

    # 得到当前用户的关系
    relations = Relationship.relate.filter(user__id=uid)
    print(relations)
    # 得到当前用户作为朋友的关系
    contary_relations = Relationship.relate.filter(friend__id=uid)

    for relation in relations:
        # 找出朋友的关系
        poss_relations = Relationship.relate.filter(user__id=relation.friend.id)
        print(poss_relations)
        poss_list = []

        for poss in poss_relations:
            poss_list.append(poss.friend)
            # print(poss.friend)

        possible.update({relation.friend:poss_list})

    print(possible)
    friend = []
    for key in possible:
        item = key.account_number
        for p in possible[key]:
            friend.append(p.account_number)
    print(friend)


    # 反向寻找
    possible = {}
    for relation in contary_relations:
        poss_relations = Relationship.relate.filter(friend__id=relation.user.id)
        poss_list = []
        for poss in poss_relations:
            poss_list.append(poss.user)

        possible.update({relation.friend: poss_list})

    for key in possible:
        item = key.account_number
        for p in possible[key]:
            friend.append(p.account_number)

    # 还需要增加一个判断：即如果潜在好友已经成为了直接好友。需要排除在外

    for relation in relations:
        for f in friend:
            if relation.friend.account_number == f:
                friend.remove(f)
    print(friend)
    possible_count = len(friend)

    context.update({'possable':friend})
    context.update({'possible_count':possible_count})

    return render(request, 'possible_massage.html', context=context)

def delete_friend(request):
    # 删除好友
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
        'count': len(friends_list),
    }
    post = request.POST
    friend_number = post.get('friendID')
    print(friend_number)
    friend = Ordinary_User.users.get(account_number=friend_number)
    relation = Relationship.relate.get(friend__id=friend.id)
    relation.delete()

    return redirect('user:index_for_user')

def load_image(request):
    image = request.FILES.get('image')
    print('load:')
    print(image)
    uid = request.session.get('uid', default=None)
    user = Ordinary_User.users.get(id=uid)

    return redirect('user:index_for_user')

def friend_examine(request):
    uid = request.session.get('uid', default=None)
    user = Ordinary_User.users.get(id=uid)
    friends = get(request)
    id_list = []
    friends_list = []
    f_list = []
    if friends['msg'] == 'OK':
        for item in friends['data']:
            id_list.append(item['friend_id'])

    for i in id_list:
        u = Ordinary_User.users.get(id=i)
        friends_list.append(u.account_number)
        f_list.append(u)
    # 记录一下未通过审核的人的id
    no = []
    relations = Relationship.relate.filter(friend_id=uid, if_pass=False)
    for relation in relations:
        no.append(relation.user)

    context = {
        'uname': user.account_number,
        'friends': friends,
        'account_number': friends_list,
        'count': len(friends_list),
        'avatar': user.avatar,
        'no':no,
        'f':f_list,
    }

    return render(request, 'friend_examine.html', context)

def accept_apply(request):
    uid = request.session.get('uid', default=None)
    friend_number = request.GET.get('number')
    print(friend_number)
    print(uid)
    relation = Relationship.relate.get(friend__id=uid,
                                       user__account_number=friend_number)

    relation.if_pass = True
    relation.save()

    return redirect('user:index_for_user')

def view_personal(request):
    uid = request.session.get('uid', default=None)
    user = Ordinary_User.users.get(id=uid)
    friends = get(request)
    id_list = []
    friends_list = []
    f_list = []
    if friends['msg'] == 'OK':
        for item in friends['data']:
            id_list.append(item['friend_id'])

    for i in id_list:
        u = Ordinary_User.users.get(id=i)
        friends_list.append(u.account_number)
        f_list.append(u)
    context = {
        'uname': user.account_number,
        'me': user,
        'account_number': friends_list,
        'count': len(friends_list),
        'avatar': user.avatar,
        'f': f_list,
    }
    return render(request, 'view_personal.html', context)
