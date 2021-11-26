from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("<int:pk>/", views.product_detail_view, name="detail"),  # 상품 디테일
    path("create/", views.CreateProductView.as_view(), name="create"),  # 상품 생성
    path("<int:pk>/update/", views.UpdateProductView.as_view(), name="update"),  # 상품 수정
    path("<int:pk>/delete/", views.DeleteProductView.as_view(), name="delete"),  # 상품 삭제
    path("manage/", views.ProductManageView.as_view(), name="manage"),  # 상품 관리페이지
]
