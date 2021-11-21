from django.shortcuts import render
from django.db import transaction
from django.views.generic import FormView
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from . import models
from products import models as product_models
from . import forms


def create_order(request, pk):
    try:
        if request.method == "POST":
            form = forms.CreateOrderForm(request.POST)
            product = product_models.Product.objects.get(pk=pk)
            if not product:
                return redirect(reverse("core:home"))
            if form.is_valid():
                order = form.save(commit=False)
                order.product = product
                order.user = request.user
                order.delivery = False
                number = form.cleaned_data["number"]
                product.inventory -= number
                if product.inventory < 0:
                    raise InventoryException()
                with transaction.atomic():  # 모든 처리 과정 후, 재고 저장 및 주문 저장은 하나의 트랜잭션에서 관리
                    product.save()
                    order.save()
                messages.success(request, "product ordered")
                return redirect(reverse_lazy("products:detail", kwargs={"pk": pk}))

        else:
            form = forms.CreateOrderForm()
            product = product_models.Product.objects.get(pk=pk)
        return render(request, "orders/order_create.html", {"form": form, "pk": pk})
    except InventoryException:
        return render(request, "orders/order_create.html", {"form": form, "pk": pk})


class InventoryException(Exception):
    pass
