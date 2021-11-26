from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("<int:pk>/create/", views.create_order, name="create"),  # 주문 생성
    path("<int:pk>/detail/", views.order_detail, name="detail"),  # 주문 디테일
    path("<int:pk>/update/", views.order_update, name="update"),  # 주문 수정
    path("<int:pk>/delete/", views.order_delete, name="delete"),  # 주문 삭제
    path("manage/", views.OrderManageView.as_view(), name="manage"),  # 주문 관리 페이지
    path(
        "<int:pk>/delivery/", views.order_delivery, name="delivery"
    ),  # 주문 관리 (staff 유저가 배송처리함)
    path("my_order/", views.my_order_view, name="my_order"),  # 내가 한 주문
]
