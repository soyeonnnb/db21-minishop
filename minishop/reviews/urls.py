from django.urls import path

from . import views

app_name = "reviews"

urlpatterns = [
    path("<int:order_pk>/create", views.review_create, name="create"),  # 리뷰 생성
    path("<int:pk>/update", views.ReviewUpdate.as_view(), name="update"),  # 리뷰 수정
    path("<int:pk>/delete", views.DeleteReviewView.as_view(), name="delete"),  # 리뷰 삭제
    path("my_review", views.my_review_view, name="my_review"),  # 내가 작성한 리뷰 보기
]
