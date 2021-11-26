from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView, DeleteView

from . import forms
from . import models
from users import mixins as users_mixins
from orders import models as order_models


# 리뷰 생성 함수
@login_required
def review_create(request, order_pk):
    order = order_models.Order.objects.get(
        pk=order_pk
    )  # order table에서 pk값으로 필요한 인스턴스를 가져옴
    user = request.user  # user는 요청을 보낸 유저
    if order.user != user:  # order 에 fk로 있는 user와 요청을 보낸 유저가 다르다면
        messages.error(request, "접근 권한이 없습니다.")  # 에러 == 리뷰 생성 불가
        return redirect("core:home")
    if request.method == "POST":
        form = forms.CreateReviewForm(request.POST)  # 사용자가 입력한 폼을 가져옴
        if form.is_valid():
            finished_form = form.save(commit=False)
            finished_form.user = request.user  # 폼에 없는 요소들을 채워줌
            finished_form.order = order
            finished_form.product = order.product
            finished_form.save()
            return redirect("reviews:my_review")
    else:
        form = forms.CreateReviewForm()
    return render(request, "reviews/review_create.html", {"form": form, "order": order})


# 내가 작성한 리뷰들을 봄
@login_required
def my_review_view(request):
    user = request.user
    review_list = models.Review.objects.filter(user=user).order_by(
        "-created_at"
    )  # review에서 user가 요청을 보낸 유저와 같은 리뷰를 가져와 최근에 작성한 순으로 정렬
    paginator = Paginator(review_list, 15)
    page_num = request.GET.get("page")
    review_list = paginator.get_page(page_num)
    return render(request, "reviews/review_list.html", {"review_list": review_list})


# 리뷰 수정 클래스
class ReviewUpdate(users_mixins.LoggedInOnlyView, UpdateView):

    model = models.Review  # 해당 테이블의 인스턴스를 수정함
    template_name = "reviews/review_update.html"
    fields = ("review", "rating")  # 사용자가 입력할 필드

    # object 가져오기
    def get_object(self, queryset=None):
        review = super().get_object(queryset=queryset)
        if review.user.pk != self.request.user.pk:  # review를 작성한 유저와 요청을 보낸 유저가 다르면
            return redirect("core:home")  # 홈으로 감
        return review

    def get_success_url(self):
        return reverse("reviews:my_review")

    # 폼 입력 커스텀
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


# 리뷰 삭제 클래스
class DeleteReviewView(users_mixins.LoggedInOnlyView, DeleteView):

    model = models.Review  # 해당 테이블의 인스턴스 삭제
    context_object_name = "reviews"

    # 성공 시 redirect 할 url
    def get_success_url(self):
        return reverse_lazy("reviews:my_review")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
