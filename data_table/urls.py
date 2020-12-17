from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

app_name = 'data_table'

urlpatterns = [
    url(r'^show_date/', views.view_table, name='show_date'),
    url(r'^add_task/', views.add_table, name='add_task'),
    url(r'^add_page/', TemplateView.as_view(template_name='add_task.html'), name='add_page'),
    url(r'^view_tables/', views.view_tables, name='view_tables'),
    url(r'^change_status/', views.change_status, name='change_status'),
    url(r'view_finished/', views.view_finished, name='view_finished'),
    url(r'delete_task/', views.delete_task, name='delete_task'),
]