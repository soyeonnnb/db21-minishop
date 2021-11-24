from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.shortcuts import redirect

from . import models
from products import models as product_model

# Create your views here.
@login_required
def my_wish_view(request):
    user = request.user
    wish_list = models.Wish.objects.filter(user=user).order_by("-added_date")
    paginator = Paginator(wish_list, 15)
    page_num = request.GET.get("page")
    wish_list = paginator.get_page(page_num)
    return render(request, "wishs/wish_list.html", {"wish_list": wish_list})


@login_required
def add_wish(request, pk):
    user = request.user
    product = product_model.Product.objects.get(pk=pk)
    wish = models.Wish()
    wish.user = user
    wish.product = product
    wish.added_date = timezone.now()
    wish.save()
    return redirect("products:detail", pk)


@login_required
def delete_wish(request, pk):
    user = request.user
    product = product_model.Product.objects.get(pk=pk)
    wish = models.Wish.objects.get(user=user, product=product)
    wish.delete()
    return redirect("products:detail", pk)
