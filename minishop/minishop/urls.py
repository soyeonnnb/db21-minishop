from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# 해당 프로젝트의 url 모음
urlpatterns = [
    path("", include("core.urls", namespace="core")),
    path("wishs/", include("wishs.urls", namespace="wishs")),
    path("products/", include("products.urls", namespace="products")),
    path("users/", include("users.urls", namespace="users")),
    path("orders/", include("orders.urls", namespace="orders")),
    path("board/", include("board.urls", namespace="board")),
    path("reviews/", include("reviews.urls", namespace="reviews")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
