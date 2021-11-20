from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse

# Create your views here.
def my_page(request):
    pass


def logout_view(request):
    logout(request)
    return redirect(reverse("core:home"))


def login(request):
    pass
