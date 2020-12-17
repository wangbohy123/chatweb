from . import views
from django.conf.urls import url,include

app_name = 'chat'

urlpatterns = [
    url(r'^get_massage/', views.get_massage, name='get_massage'),
    url(r'^show_room/', views.show_room, name='show_room'),
    url(r'^send_massage/', views.send_massage, name='send_massage'),
]