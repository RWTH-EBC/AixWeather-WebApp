from django.urls import path
from .views import index_view
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

app_name="utc_converter"
urlpatterns = [
    path('utc_converter/', index_view, name="main"),
    
]
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
