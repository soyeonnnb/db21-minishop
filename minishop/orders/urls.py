from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [path("create/<int:pk>/", views.create_order, name="create")]
