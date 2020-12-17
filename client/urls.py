from . import views
from django.conf.urls import url,include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'client'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/$',views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^longin_handel/$', views.login_handel, name='longin_handel'),
    url(r'^register_handel/$', views.register_handel, name='register_handel'),
    url(r'^del_session/$', views.del_session, name='del_session'),
    url(r'^verifycode$', views.verifycode, name='verifycode'),
    url(r'^index_for_user/$', views.index_for_user, name='index_for_user'),
    url(r'^friends_config/',views.friends_config, name='friend_config'),
    url(r'^show_friend/', views.view_friend, name='show_friend'),
    url(r'^add_friend/', views.add_friend, name='add_friend'),
    url(r'^find_friend/', views.find_friend, name='find_friend'),
    url(r'^add_page/', views.add_page, name='add_page'),
    url(r'^delete_friend/', views.delete_friend, name='delete_friend'),
    url(r'^load_file/', TemplateView.as_view(template_name='load_file.html'), name='load_file'),
    url(r'^load_image/', views.load_image, name='load_image'),
    url(r'^friend_examine/', views.friend_examine, name='friend_examine'),
    url(r'^accept_apply/', views.accept_apply, name='accept_apply'),
    url(r'view_personal/', views.view_personal, name='view_personal'),
]

