from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.models import AnonymousUser
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.core.paginator import Paginator


from . import models
from . import forms
from users import mixins as users_mixins
from wishs import models as wishs_models

# Create your views here.
class HomeView(ListView):

    """HomeView Definition"""

    model = models.Product
    paginate_by = 12
    paginate_orphans = 4
    ordering = "-created_at"
    context_object_name = "products"


# 상품 상세페이지
def product_detail_view(request, pk):
    user = request.user
    product = models.Product.objects.get(pk=pk)
    if user != AnonymousUser():
        try:
            wishs_models.Wish.objects.get(user=user, product=product)
            is_wish = True
        except wishs_models.Wish.DoesNotExist:
            is_wish = False
    else:
        is_wish = False
    return render(
        request,
        "products/product_detail.html",
        {"product": product, "is_wish": is_wish},
    )


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
    success_message = "상품이 수정되었습니다"
    # 폼 입력방식 커스텀
    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["name"].widget.attrs = {
            "placeholder": "상품명",
            "class": "form-control",
            "id": "nameInput",
            "aria-describedby": "nameInput",
            "aria-label": "Name",
            "type": "text",
        }
        form.fields["price"].widget.attrs = {
            "class": "form-control",
            "id": "priceInput",
            "aria-describedby": "priceInput",
            "aria-label": "Price",
            "min": 0,
        }
        form.fields["inventory"].widget.attrs = {
            "class": "form-control",
            "id": "inventoryInput",
            "aria-describedby": "inventoryInput",
            "aria-label": "Inventory",
            "min": 0,
        }
        form.fields["description"].widget.attrs = {
            "class": "form-control",
            "id": "descriptionInput",
            "aria-describedby": "descriptionInput",
            "aria-label": "Description",
        }
        form.fields["categories"].widget.attrs = {
            "class": "form-select",
            "id": "categoriesInput",
            "aria-describedby": "categoriesInput",
            "aria-label": "Categories",
        }
        form.fields["photo"].widget.attrs = {
            "class": "form-control",
            "id": "photoInput",
        }

        form.fields["discountinue"].widget.attrs = {
            "class": "form-check-input",
            "type": "checkbox",
            "id": "discountinueInput",
            "aria-describedby": "discountinueInput",
            "aria-label": "Discountinue",
        }
        return form

    def get_success_url(self):
        return reverse("products:manage")


@method_decorator(staff_member_required, name="dispatch")
class DeleteProductView(users_mixins.LoggedInOnlyView, DeleteView):

    model = models.Product
    context_object_name = "product"

    def get_success_url(self):
        return reverse_lazy("products:manage")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


@method_decorator(staff_member_required, name="dispatch")
class ProductManageView(ListView):

    model = models.Product
    paginate_by = 15
    paginate_orphans = 4
    ordering = "-created_at"
    context_object_name = "product_list"
    template_name = "products/product_manage.html"
