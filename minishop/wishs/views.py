from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.utils import timezone

from . import models
from products import models as product_model


# 내가 찜한 목록
@login_required
def my_wish_view(request):
    user = request.user
    wish_list = models.Wish.objects.filter(user=user).order_by(
        "-added_date"
    )  # Wish table 에서 user=user인 인스턴스 집합을 가져와 최근에 생성한 순으로 정렬
    paginator = Paginator(wish_list, 15)
    page_num = request.GET.get("page")
    wish_list = paginator.get_page(page_num)
    return render(request, "wishs/wish_list.html", {"wish_list": wish_list})


# wish 인스턴스 생성(찜하기)
@login_required
def add_wish(request, pk):
    user = request.user
    product = product_model.Product.objects.get(
        pk=pk
    )  # Product table에서 pk로 product 인스턴스를 가져옴
    wish = models.Wish()  # 아무것도 입력되지 않은 wish 인스턴스 생성
    wish.user = user  # 애트리뷰트에 값 입력
    wish.product = product
    wish.added_date = timezone.now()
    wish.save()  # DB에 저장
    return redirect("products:detail", pk)


# wish 인스턴스 삭제(찜 취소)
@login_required
def delete_wish(request, pk):
    user = request.user  # 요청을 보낸 user
    product = product_model.Product.objects.get(
        pk=pk
    )  # Product table에서 pk로 product 인스턴스를 가져옴
    wish = models.Wish.objects.get(
        user=user, product=product
    )  # wish table에서 user=user, product=product인 인스턴스를 가져옴
    wish.delete()  # 해당 인스턴스 삭제
    return redirect("products:detail", pk)
