from django.urls import path
from . import views
from converter import views as converterviews
app_name = 'templateapp'
urlpatterns = [
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'), 
    path('privacypolicy/', views.privacypolicy, name='privacypolicy'),]
