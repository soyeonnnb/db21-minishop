from django.urls import path

from . import views

app_name = "wishs"

urlpatterns = [
    path("<int:pk>/add/", views.add_wish, name="add"),
    path("<int:pk>/delete/", views.delete_wish, name="delete"),
    path("my_wish/", views.my_wish_view, name="my_wish"),
]
