from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import FormView, UpdateView


from . import forms
from . import models
from .mixins import LoggedInOnlyView


# 로그아웃 method
def logout_view(request):
    logout(request)
    return redirect(reverse("core:home"))  # 로그아웃 성공시 갈 url


# 로그인 method
class UserLoginView(View):
    # method 가 get일 경우
    def get(self, request):
        form = forms.LoginForm()
        return render(request, "users/login.html", {"form": form})

    # method 가 post일 경우
    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None:  # authenticate 했을 경우에 user 가 None이 아니라면
                login(request, user)  # login 해서
                return redirect(reverse("core:home"))  # home 으로 이동
        return render(request, "users/login.html", {"form": form})


# 유저 정보 보기
@login_required
def my_info(request):
    user = request.user
    user_info = get_object_or_404(
        models.User, pk=user.pk
    )  # User 테이블에서 user=request.user 인 정보를 가져옴
    return render(request, "users/my_info.html", {"user_info": user_info})


# 회원가입 클래스
class SignUpView(FormView):

    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("users:login")

    # form 이 vaild해야 저장
    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, email=email, password=password)
        if user is not None:  # 유저가 회원가입에 성공하면 로그인 상태로 redirect 됨
            login(self.request, user)
        return super().form_valid(form)


# 회원정보 수정 클래스
class UserUpdateView(UpdateView, LoggedInOnlyView):

    """UserUpdate View Definition"""

    model = models.User  # 해당 Table의 인스턴스를 수정
    template_name = "users/update.html"
    fields = (
        "nickname",
        "gender",
        "birth",
        "mobile",
    )
    success_url = reverse_lazy("users:my_info")

    def get_object(self, queryset=None):
        return self.request.user

    # 폼 입력방식 커스텀
    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["nickname"].widget.attrs = {
            "placeholder": "Nickname",
            "class": "form-control",
            "id": "nicknameInput",
            "aria-describedby": "nicknameInput",
            "aria-label": "Nickname",
            "type": "text",
        }
        form.fields["gender"].widget.attrs = {
            "class": "form-select",
            "id": "genderInput",
            "aria-describedby": "genderInput",
            "aria-label": "Gender",
        }
        form.fields["birth"].widget.attrs = {
            "placeholder": "2000-01-01",
            "class": "form-control",
            "id": "birthInput",
            "aria-describedby": "birthInput",
            "aria-label": "Birth",
        }
        form.fields["mobile"].widget.attrs = {
            "placeholder": "01234567890",
            "class": "form-control",
            "id": "mobileInput",
            "aria-describedby": "mobileInput",
            "aria-label": "Mobile",
        }
        return form
