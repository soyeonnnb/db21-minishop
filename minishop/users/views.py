from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, UpdateView

from . import forms
from . import models
from .mixins import LoggedInOnlyView


# 로그아웃 method
def logout_view(request):
    logout(request)
    return redirect(reverse("core:home"))


# 로그인 method
class LoginView(FormView):

    template_name = "users/login.html"
    success_url = reverse_lazy("core:home")
    form_class = forms.LoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


@login_required
def my_page(request):
    user = request.user
    user_info = get_object_or_404(models.User, pk=user.pk)
    return render(request, "users/my_page.html", {"user_info": user_info})


class SignUpView(FormView):

    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    # form 이 vaild해야 저장
    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, email=email, password=password)
        # 나중에 고치기
        print(user)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


class UserUpdateView(UpdateView, LoggedInOnlyView):

    """UserUpdate View Definition"""

    model = models.User
    template_name = "users/update.html"
    fields = (
        "nickname",
        "gender",
        "birth",
        "mobile",
    )
    success_url = reverse_lazy("users:my_page")

    def get_object(self, queryset=None):
        return self.request.user
