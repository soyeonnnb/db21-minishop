from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("my_info/", views.my_info, name="my_info"),  # 내 정보 보기
    path("logout/", views.logout_view, name="logout"),  # 로그아웃
    path("login/", views.UserLoginView.as_view(), name="login"),  # 로그인
    path("sign_up/", views.SignUpView.as_view(), name="sign_up"),  # 회원가입
    path("update/", views.UserUpdateView.as_view(), name="update"),  # 회원정보 수정
]
