from django.urls import re_path
from . import views
from converter import views as converterviews
app_name = 'templateapp'
urlpatterns = [
    re_path(r'progressurl', views.progressurl, name='progressurl'),
    re_path(r'about', views.about, name='about'),
    re_path(r'contact', views.contact, name='contact'), 
    re_path(r'result', views.result, name='result'),
    re_path(r'privacypolicy', views.privacypolicy, name='privacypolicy'),]
