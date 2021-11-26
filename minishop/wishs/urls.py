from django.urls import path

from . import views

app_name = "wishs"

urlpatterns = [
    path("<int:pk>/add/", views.add_wish, name="add"),  # 찜 하기
    path("<int:pk>/delete/", views.delete_wish, name="delete"),  # 찜 취소
    path("my_wish/", views.my_wish_view, name="my_wish"),  # 내가 찜한 목록
]
