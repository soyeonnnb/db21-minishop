from django.contrib.auth.models import AnonymousUser
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)


from . import models
from . import forms
from users import mixins as users_mixins
from wishs import models as wishs_models
from reviews import models as reviews_model

# 홈 페이지.
class HomeView(ListView):

    """HomeView Definition"""

    model = models.Product  # 해당 테이블의 값을 가져옴
    paginate_by = 12
    paginate_orphans = 4
    ordering = "-created_at"
    context_object_name = "products"


# 상품 상세페이지
def product_detail_view(request, pk):
    user = request.user
    product = models.Product.objects.get(pk=pk)
    if user != AnonymousUser():  # 만약 비로그인 회원이 아니라면
        try:
            wishs_models.Wish.objects.get(
                user=user, product=product
            )  # wish 테이블에서 user=user, product=product인 인스턴스를 가져옴
            is_wish = True  # 가져오면 찜하기는 true
        except wishs_models.Wish.DoesNotExist:  # 만약 위의 그러한 인스턴스가 없다면
            is_wish = False  # 찜하기는 false
    else:  # 비로그인 회원이라면
        is_wish = False  # 찜하기는 false
    reviews = reviews_model.Review.objects.filter(
        product=product
    )  # reviews 테이블에서 product=product 인 인스턴스를 가져옴
    return render(
        request,
        "products/product_detail.html",
        {"product": product, "is_wish": is_wish, "reviews": reviews},
    )


# 상품 생성 클래스. staff 유저만 접근 가능
@method_decorator(staff_member_required, name="dispatch")
class CreateProductView(CreateView):

    """Product Create View Definition"""

    model = models.Product  # 연결할 클래스 or table명
    context_object_name = "product"  # context 변수명 지정
    form_class = forms.CreateProductForm  # 우리가 만든 폼 클래스를 form_class에 할당!
    template_name = "products/product_create.html"

    def get_success_url(self):
        return reverse("products:detail", kwargs={"pk": self.object.pk})


# 상품 수정 클래스. 위와 동일하게 staff 멤버만 접근 가능
@method_decorator(staff_member_required, name="dispatch")
class UpdateProductView(users_mixins.LoggedInOnlyView, UpdateView):

    model = models.Product  # 해당 테이블의 인스턴스 수정
    template_name = "products/product_update.html"
    fields = (
        "name",
        "price",
        "inventory",
        "description",
        "category",
        "photo",
        "discontinue",
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
        form.fields["category"].widget.attrs = {
            "class": "form-select",
            "id": "categoryInput",
            "aria-describedby": "categoryInput",
            "aria-label": "Category",
        }
        form.fields["photo"].widget.attrs = {
            "class": "form-control",
            "id": "photoInput",
        }

        form.fields["discontinue"].widget.attrs = {
            "class": "form-check-input",
            "type": "checkbox",
            "id": "discontinueInput",
            "aria-describedby": "discontinueInput",
            "aria-label": "Discontinue",
        }
        return form

    def get_success_url(self):
        return reverse("products:manage")


# 상품 삭제 클래스. 위와 동일
@method_decorator(staff_member_required, name="dispatch")
class DeleteProductView(users_mixins.LoggedInOnlyView, DeleteView):

    model = models.Product  # 해당 테이블의 인스턴스 삭제
    context_object_name = "product"

    def get_success_url(self):
        return reverse_lazy("products:manage")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


# 상품 관리 클래스
@method_decorator(staff_member_required, name="dispatch")
class ProductManageView(ListView):

    model = models.Product  # 해당 테이블의 인스턴스 관리
    paginate_by = 15
    paginate_orphans = 4
    ordering = "-created_at"  # 최근 생성된 상품 순으로 정렬
    context_object_name = "product_list"
    template_name = "products/product_manage.html"
