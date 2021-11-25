from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic import UpdateView, DeleteView

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
            finished_form.product = order.product
            finished_form.save()
            return redirect("reviews:my_review")
    else:
        form = forms.CreateReviewForm()
    return render(request, "reviews/review_create.html", {"form": form, "order": order})


@login_required
def my_review_view(request):
    user = request.user
    review_list = models.Review.objects.filter(user=user).order_by("-created_at")
    paginator = Paginator(review_list, 15)
    page_num = request.GET.get("page")
    review_list = paginator.get_page(page_num)
    return render(request, "reviews/review_list.html", {"review_list": review_list})


class ReviewUpdate(UpdateView):

    model = models.Review
    template_name = "reviews/review_update.html"
    fields = ("review", "rating")

    def get_object(self, queryset=None):
        review = super().get_object(queryset=queryset)
        if review.user.pk != self.request.user.pk:
            return redirect("core:home")
        return review

    def get_success_url(self):
        return reverse("reviews:my_review")

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["review"].widget.attrs = {
            "placeholder": "리뷰 입력",
            "class": "form-control",
            "id": "reviewInput",
            "aria-describedby": "reviewInput",
            "aria-label": "Review",
            "type": "text",
        }
        form.fields["rating"].widget.attrs = {
            "class": "form-control",
            "id": "ratingInput",
            "aria-describedby": "ratingInput",
            "aria-label": "Rating",
            "min": 1,
            "max": 5,
        }
        return form


class DeleteReviewView(DeleteView):

    model = models.Review
    context_object_name = "reviews"

    def get_success_url(self):
        return reverse_lazy("reviews:my_review")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
