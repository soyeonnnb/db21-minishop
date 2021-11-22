from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


class LoggedInOnlyView(LoginRequiredMixin):

    login_url = reverse_lazy("users:login")
