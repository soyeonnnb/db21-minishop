from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import FormView, UpdateView

from . import forms
from . import models
from . import mixins
from .mixins import LoggedInOnlyView

from products import models as product_models


# 로그아웃 method
def logout_view(request):
    logout(request)
    return redirect(reverse("core:home"))


# 로그인 method
class UserLoginView(View):
    def get(self, request):
        form = forms.LoginForm()
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            print(email, password)
            print(user)
            if user is not None:
                login(request, user)
                return redirect(reverse("core:home"))
        return render(request, "users/login.html", {"form": form})


@login_required
def my_info(request):
    user = request.user
    user_info = get_object_or_404(models.User, pk=user.pk)
    return render(request, "users/my_info.html", {"user_info": user_info})


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


@staff_member_required
def staff_view(request):
    product_list = product_models.Product.objects.all()
    return render(request, "users/staff.html", {"product_list": product_list})
