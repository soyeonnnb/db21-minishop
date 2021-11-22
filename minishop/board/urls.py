from django.urls import path
from . import views

app_name="board"

urlpatterns = [
    path("", views.FAQListView().as_view, name="list")
]
