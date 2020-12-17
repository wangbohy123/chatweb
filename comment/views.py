from django.shortcuts import render, redirect
from django.http import *
from client.models import Ordinary_User
from .models import Comment


def show_comments(request):
    uid = request.session.get('uid', default=None)
    user = Ordinary_User.users.get(id=uid)
    # 得到发给当前用户的留言
    comments = Comment.comments.filter(recevier__id=uid)
    length = len(comments)
    context = {
        'user':user,
        'comments':comments,
        'length':length,
    }
    return render(request, 'comment.html', context=context)

def view_friend_comment(request):
    uid = request.session.get('uid', default=None)
    user = Ordinary_User.users.get(id=uid)

    if request.method == 'POST':
        post = request.POST
        friend = post.get('friend')
        comments = Comment.comments.filter(recevier__account_number=friend)
        # print(len(comments))
        length = len(comments)

        # print(length)
        contxt = {
            'user':user,
            'comments':comments,
            'length':length,
            'receiver':friend
        }

    else:
        return HttpResponseBadRequest

    return render(request, 'comment.html', contxt)

def send_comment(request):
    post = request.POST
    receiver = post.get('receiver')
    receiver = Ordinary_User.users.get(account_number=receiver)
    sender = post.get('sender')
    sender = Ordinary_User.users.get(account_number=sender)
    message = post.get('message')
    comment = Comment.comments.create(recevier=receiver, sender=sender, saying=message)
    return redirect('user:index_for_user')
