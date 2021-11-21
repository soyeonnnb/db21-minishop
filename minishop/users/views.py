from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView

from . import forms

# Create your views here.
def my_page(request):
    pass


def logout_view(request):
    logout(request)
    return redirect(reverse("core:home"))


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
