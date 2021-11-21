from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("my_page/", views.my_page, name="my_page"),  # 추후 추가
    path("logout/", views.logout_view, name="logout"),  # 로그아웃 url
    path("login/", views.LoginView.as_view(), name="login"),  # 로그인 url
]
