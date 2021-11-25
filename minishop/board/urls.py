from django.urls import path
from . import views

app_name = "board"

urlpatterns = [
    path("", views.FAQListView.as_view(), name="list"),
    path("create/", views.faq_post_create, name="create"),
    path("my_faq/", views.my_faqpost_view, name="my_faq"),
    path("<int:pk>/detail/", views.faq_post_detail, name="detail"),
    path("<int:pk>/update/", views.UpdatePostView.as_view(), name="update"),
    path("<int:pk>/comment_create/", views.faqcomment_create, name="comment_create"),
]
