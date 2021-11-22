from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy, reverse


from . import models
from . import forms
from users import mixins as users_mixins

# Create your views here.
class HomeView(ListView):

    """HomeView Definition"""

    model = models.Product
    paginate_by = 12
    paginate_orphans = 4
    ordering = "created_at"
    context_object_name = "products"


class ProductDetailView(DetailView):

    """Product Detail View Definition"""

    model = models.Product


@method_decorator(staff_member_required, name="dispatch")
class CreateProductView(CreateView):

    """Product Create View Definition"""

    model = models.Product  # 연결할 클래스 or table명
    context_object_name = "product"  # context 변수명 지정
    form_class = forms.CreateProductForm  # 우리가 만든 폼 클래스를 form_class에 할당!
    template_name = "products/product_create.html"

    def get_success_url(self):
        return reverse("products:detail", kwargs={"pk": self.object.pk})


@method_decorator(staff_member_required, name="dispatch")
class UpdateProductView(users_mixins.LoggedInOnlyView, UpdateView):

    model = models.Product
    template_name = "products/product_update.html"
    fields = (
        "name",
        "price",
        "inventory",
        "description",
        "categories",
        "photo",
        "discountinue",
    )
    success_message = "Product Updated"


@method_decorator(staff_member_required, name="dispatch")
class DeleteProductView(users_mixins.LoggedInOnlyView, DeleteView):

    model = models.Product
    context_object_name = "product"

    def get_success_url(self):
        return reverse_lazy("users:staff")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
