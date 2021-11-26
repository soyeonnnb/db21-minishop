from django.urls import path
from products import views as products_views

app_name = "core"

urlpatterns = [path("", products_views.HomeView.as_view(), name="home")]  # home 화면
