from django.urls import path

from . import views

app_name = "reviews"

urlpatterns = [
    path("<int:order_pk>/create", views.review_create, name="create"),
    path("<int:pk>/update", views.ReviewUpdate.as_view(), name="update"),
    path("<int:pk>/delete", views.DeleteReviewView.as_view(), name="delete"),
    path("my_review", views.my_review_view, name="my_review"),
]
