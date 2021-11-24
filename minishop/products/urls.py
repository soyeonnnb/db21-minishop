from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("<int:pk>/", views.product_detail_view, name="detail"),
    path("create/", views.CreateProductView.as_view(), name="create"),
    path("<int:pk>/update/", views.UpdateProductView.as_view(), name="update"),
    path("<int:pk>/delete/", views.DeleteProductView.as_view(), name="delete"),
    path("manage/", views.ProductManageView.as_view(), name="manage"),
]
