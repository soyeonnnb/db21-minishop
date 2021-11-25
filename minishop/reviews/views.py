from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from . import forms
from . import models
from orders import models as order_models

# Create your views here.


@login_required
def review_create(request, order_pk):
    order = order_models.Order.objects.get(pk=order_pk)
    user = request.user
    if order.user != user:
        messages.error(request, "접근 권한이 없습니다.")
        return redirect("core:home")
    if request.method == "POST":
        form = forms.CreateReviewForm(request.POST)
        if form.is_valid():
            finished_form = form.save(commit=False)
            finished_form.user = request.user
            finished_form.order = order
            finished_form.save()
            return redirect(
                "board:detail",
                finished_form.pk,
            )
    else:
        form = forms.CreateReviewForm()
    return render(request, "reviews/review_create.html", {"form": form, "order": order})
