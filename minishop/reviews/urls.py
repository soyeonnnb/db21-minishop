from django.urls import path

from . import views

app_name = "reviews"

urlpatterns = [
    path("<int:order_pk>/create", views.review_create, name="create"),
]
