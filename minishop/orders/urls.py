from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("<int:pk>/create/", views.create_order, name="create"),
    path("<int:pk>/detail/", views.order_detail, name="detail"),
    path("<int:pk>/update/", views.order_update, name="update"),
    path("<int:pk>/delete/", views.order_delete, name="delete"),
    path("manage/", views.OrderManageView.as_view(), name="manage"),
    path("<int:pk>/delivery/", views.order_delivery, name="delivery"),
    path("my_order/", views.my_order_view, name="my_order"),
]
