from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("my_page/", views.my_page, name="my_page"),
    path("logout/", views.logout, name="logout"),
    path("login/", views.login, name="login"),
]
