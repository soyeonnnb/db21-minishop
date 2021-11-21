from django.shortcuts import render
from django.views.generic import FormView
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from . import models
from products import models as product_models
from . import forms


def create_order(request, pk):
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
            order.save()
            messages.success(request, "product ordered")
            return redirect(reverse("products:detail", kwargs={"pk": pk}))

    else:
        form = forms.CreateOrderForm()
        product = product_models.Product.objects.get(pk=pk)
    return render(request, "orders/order_create.html", {"form": form, "pk": pk})
