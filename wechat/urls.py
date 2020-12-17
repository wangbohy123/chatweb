"""wechat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from client.views import index
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index),
    url(r'^user/', include('client.urls', namespace='user')),
    url(r'^user_center/', include('user_center.urls', namespace='user_center')),
    url(r'^chat/', include('chat.urls', namespace='chat')),
    url(r'^comment/', include('comment.urls', namespace='comment')),
    url(r'^date/', include('data_table.urls', namespace='date'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
