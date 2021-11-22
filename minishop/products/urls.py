from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("<int:pk>/", views.ProductDetailView.as_view(), name="detail"),
    path("create/", views.CreateProductView.as_view(), name="create"),
]
