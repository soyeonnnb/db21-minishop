from django.urls import path
from . import views

app_name = "board"

urlpatterns = [
    path("", views.FAQListView.as_view(), name="list"),  # faq 글 목록
    path("create/", views.faq_post_create, name="create"),  # faq 글 생성
    path("my_faq/", views.my_faqpost_view, name="my_faq"),  # 내가 작성한 faq 글 목록
    path("<int:pk>/detail/", views.faq_post_detail, name="detail"),  # faq 글 상세히 보기
    path("<int:pk>/update/", views.faq_post_update, name="update"),  # faq 글 수정
    path("<int:pk>/delete/", views.DeletePostView.as_view(), name="delete"),  # faq 글 삭제
    path(
        "<int:pk>/comment_create/", views.faqcomment_create, name="comment_create"
    ),  # faq 답글 작성
]
