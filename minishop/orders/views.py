from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView

from . import models
from . import forms

from users import mixins as users_mixins
from products import models as product_models

# 주문하기 함수
@login_required
def create_order(request, pk):
    try:
        if request.method == "POST":
            form = forms.CreateOrderForm(request.POST)
            product = product_models.Product.objects.get(pk=pk)
            if not product:
                return redirect(reverse("core:home"))
            if form.is_valid():
                with transaction.atomic():  # 모든 처리 과정 후, 재고 저장 및 주문 저장은 하나의 트랜잭션에서 관리
                    order = form.save(commit=False)
                    order.product = product
                    order.user = request.user
                    order.delivery = False
                    number = form.cleaned_data["number"]
                    product.inventory -= number  # 상품의 재고에서 수량만큼 뺌
                    if product.inventory < 0:  # 상품의 재고는 (-)가 될 수 없으므로 재고 에러를 발생시킴
                        raise InventoryException()
                    product.save()  # 재고가 (+) 라면 상품을 저장하고
                    order.save()  # 주문을 저장하는 것까지 하나의 트랜잭션에서 관리
                    messages.success(request, "product ordered")
                return redirect(reverse_lazy("products:detail", kwargs={"pk": pk}))

        else:
            form = forms.CreateOrderForm()
            product = product_models.Product.objects.get(pk=pk)
        return render(
            request,
            "orders/order_create.html",
            {"form": form, "pk": pk, "product": product},
        )
    # 재고 에러가 발생했다면
    except InventoryException:
        messages.error(request, "재고부족")
        return render(
            request,
            "orders/order_create.html",  # 주문 생성 폼에 머무르기
            {"form": form, "pk": pk, "product": product},
        )


# 재고부족 에러
class InventoryException(Exception):
    pass


# 내 주문 리스트 조회 리스트
@login_required
def my_order_view(request):
    user = request.user
    order_list = models.Order.objects.filter(user=user).order_by(
        "-date_ordered"
    )  # Order 테이블에서 user 애트리뷰트가 요청을 보낸 user와 같은 인스턴스만 가져온 후 최근에 주문한 것부터 가져옴
    paginator = Paginator(order_list, 15)
    page_num = request.GET.get("page")
    order_list = paginator.get_page(page_num)
    return render(request, "orders/order_list.html", {"order_list": order_list})


# 주문 디테일 조회 클래스
class OrderDetailView(users_mixins.LoggedInOnlyView, DetailView):

    model = models.Order


@login_required
def order_detail(request, pk):
    user = request.user
    order = models.Order.objects.get(pk=pk)  # 주문의 pk가 요청을 보낸 pk와 같은 인스턴스를 가져옴.
    if user == order.user or user.is_staff == True:  # 주문자와 staff유저만 해당 주문 디테일을 볼 수 있음.
        return render(request, "orders/order_detail.html", {"order": order})
    else:
        messages.error(request, "접근 권한이 없습니다.")
        return reverse_lazy("core:home")


# 주문 수정 함수
@login_required
def order_update(request, pk):
    order = models.Order.objects.get(pk=pk)
    product = product_models.Product.objects.get(
        pk=order.product.pk
    )  # order를 보낸 product pk로 product 테이블에서 인스턴스를 찾음
    try:
        if request.method == "POST":
            form = forms.UpdateOrderForm(request.POST)
            if not product:
                return redirect(reverse("core:home"))
            if form.is_valid():
                with transaction.atomic():  # 모든 처리 과정 후, 재고 저장 및 주문 저장은 하나의 트랜잭션에서 관리
                    # order = form.save(commit=False)
                    number = form.cleaned_data["number"]
                    method = form.cleaned_data["method"]
                    address = form.cleaned_data["address"]
                    product.inventory += order.number  # 이전에 주문한 수량만큼 product의 인벤토리에 추가함
                    product.inventory -= number  # 새로운 주문 수량만큼 product의 인벤토리에서 뺌
                    if product.inventory < 0:  # 재고량은 (-)가 될 수 없으므로 재고 에러를 냄
                        raise InventoryException()
                    order.method = method  # 폼 저장
                    order.address = address
                    order.number = number
                    product.save()
                    order.save()
                    messages.success(request, "주문이 수정되었습니다.")
                return redirect(
                    reverse_lazy("orders:detail", kwargs={"pk": pk, "product": product})
                )

        else:
            order = models.Order.objects.get(pk=pk)
            form = forms.UpdateOrderForm(instance=order)
        return render(
            request,
            "orders/order_update.html",
            {"form": form, "pk": pk, "product": product},
        )
    except InventoryException:  # 이 위와 같음
        messages.error(request, "재고부족")
        return render(
            request,
            "orders/order_update.html",
            {"form": form, "pk": pk, "product": product},
        )


# 주문 취소 함수
@login_required
def order_delete(request, pk):
    order = models.Order.objects.get(pk=pk)
    if order is None:
        messages.success(request, "주문이 존재하지 않습니다.")
    product = product_models.Product.objects.get(pk=order.product.pk)
    if product is None:
        order.delete()  # 해당하는 order 인스턴스 삭제
        return redirect(reverse_lazy("orders:my_order"))
    with transaction.atomic():  # 모든 처리 과정 후, 재고 저장 및 주문 저장은 하나의 트랜잭션에서 관리
        product.inventory += order.number  # 재고에 이전에 주문한 수량만큼 더해줌
        product.save()  # product 저장
        order.delete()  # 해당하는 order 인스턴스 삭제
        messages.success(request, "주문이 삭제되었습니다.")
    return redirect(reverse_lazy("orders:my_order"))


# order 관리 페이지
@method_decorator(staff_member_required, name="dispatch")  # staff 멤버만 접근 가능
class OrderManageView(ListView):
    model = models.Order
    paginate_by = 15
    paginate_orphans = 4
    ordering = "-date_ordered"  # 최근에 주문한 순서대로 정렬
    context_object_name = "order_list"
    template_name = "orders/order_manage.html"


# staff 멤버만 배송처리 가능
@staff_member_required
def order_delivery(request, pk):
    order = models.Order.objects.get(pk=pk)
    with transaction.atomic():  # 배송을 했지만 주문에 처리가 안 될 경우를 대비해 하나의 트랜젝션에서 관리
        order.delivery = True  # delivery 처리 함
        order.save()  # 주문서 저장
        messages.success(request, "배송처리가 완료되었습니다.")
    return redirect(reverse("orders:manage"))
