from . import views
from django.conf.urls import url,include

app_name = 'user_center'

urlpatterns = [
    url(r'^show/$', views.show, name='show'),
]