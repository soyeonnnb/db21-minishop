from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("my_page/", views.my_page, name="my_page"),  # 내 정보 보기
    path("logout/", views.logout_view, name="logout"),  # 로그아웃 url
    path("login/", views.LoginView.as_view(), name="login"),  # 로그인 url
    path("sign_up/", views.SignUpView.as_view(), name="sign_up"),
    path("update/", views.UserUpdateView.as_view(), name="update"),
    path("staff/", views.staff_view, name="staff"),
]
