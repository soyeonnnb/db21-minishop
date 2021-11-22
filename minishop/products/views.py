from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy, reverse


from . import models
from . import forms

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
