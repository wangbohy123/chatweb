from django.views.generic import TemplateView
from django.conf.urls import url
from . import views

app_name = 'comment'

urlpatterns = [
    url(r'^show_comment/', views.show_comments, name='show_comment'),
    url(r'^view_friend_comment/', views.view_friend_comment, name='view_friend_comment'),
    url(r'^send_comment/', views.send_comment, name='send_comment'),
]