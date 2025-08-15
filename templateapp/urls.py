from django.urls import path
from . import views

app_name = "templateapp"
urlpatterns = [
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("impressum/", views.impressum, name="impressum"),
]
