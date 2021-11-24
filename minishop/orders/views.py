from django.shortcuts import render
from django.db import transaction
from django.views.generic import DetailView
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator

from . import models
from . import forms
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
                    product.inventory -= number
                    if product.inventory < 0:
                        raise InventoryException()
                    product.save()
                    order.save()
                messages.success(request, "product ordered")
                return redirect(reverse_lazy("products:detail", kwargs={"pk": pk}))

        else:
            form = forms.CreateOrderForm()
            product = product_models.Product.objects.get(pk=pk)
        return render(request, "orders/order_create.html", {"form": form, "pk": pk})
    except InventoryException:
        messages.error(request, "재고부족")
        return render(request, "orders/order_create.html", {"form": form, "pk": pk})


# 재고부족 에러
class InventoryException(Exception):
    pass


# 내 주문 리스트 조회 리스트
@login_required
def my_order_view(request):
    user = request.user
    order_list = models.Order.objects.filter(user=user).order_by("-date_ordered")
    paginator = Paginator(order_list, 15)
    page_num = request.GET.get("page")
    order_list = paginator.get_page(page_num)
    return render(request, "orders/order_list.html", {"order_list": order_list})


# 주문 디테일 조회 클래스
@method_decorator(login_required, name="dispatch")
class OrderDetailView(DetailView):

    model = models.Order


# 주문 수정 함수
def order_update(request, pk):
    try:
        if request.method == "POST":
            order = models.Order.objects.get(pk=pk)
            form = forms.UpdateOrderForm(request.POST)
            product = product_models.Product.objects.get(pk=order.product.pk)
            if not product:
                return redirect(reverse("core:home"))
            if form.is_valid():
                with transaction.atomic():  # 모든 처리 과정 후, 재고 저장 및 주문 저장은 하나의 트랜잭션에서 관리
                    # order = form.save(commit=False)
                    number = form.cleaned_data["number"]
                    method = form.cleaned_data["method"]
                    address = form.cleaned_data["address"]
                    product.inventory += order.number
                    product.inventory -= number
                    if product.inventory < 0:
                        raise InventoryException()
                    order.method = method
                    order.address = address
                    order.number = number
                    product.save()
                    order.save()
                messages.success(request, "주문이 수정되었습니다.")
                return redirect(reverse_lazy("orders:detail", kwargs={"pk": pk}))

        else:
            order = models.Order.objects.get(pk=pk)
            form = forms.UpdateOrderForm(instance=order)
        return render(request, "orders/order_update.html", {"form": form, "pk": pk})
    except InventoryException:
        messages.error(request, "재고부족")
        return render(request, "orders/order_update.html", {"form": form, "pk": pk})


# 주문 취소 함수
def order_delete(request, pk):
    order = models.Order.objects.get(pk=pk)
    if order is None:
        messages.success(request, "주문이 존재하지 않습니다.")
    product = product_models.Product.objects.get(pk=order.product.pk)
    if product is None:
        order.delete()
        return redirect(reverse_lazy("orders:my_order"))
    with transaction.atomic():  # 모든 처리 과정 후, 재고 저장 및 주문 저장은 하나의 트랜잭션에서 관리
        # order = form.save(commit=False)
        product.inventory += order.number
        product.save()
        order.delete()
        messages.success(request, "주문이 삭제되었습니다.")
    return redirect(reverse_lazy("orders:my_order"))
