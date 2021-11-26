from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# 로그인 필수 뷰 클래스
class LoggedInOnlyView(LoginRequiredMixin):

    login_url = reverse_lazy("users:login")
