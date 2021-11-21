from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):

    """Custom Order Admin"""

    fieldsets = (  # User 애트리뷰트들 분류
        (
            "Basic Info",  # 기본 정보
            {
                "fields": (
                    "user",
                    "product",
                    "number",
                    "method",
                )
            },
        ),
        (
            "Delivery",  # 추가 정보
            {
                "fields": (
                    "address",
                    "delivery",
                ),
            },
        ),
    )
    list_display = (  # 메인 화면에서 해당 애트리뷰트들 보이기
        "user",
        "product",
        "number",
        "date_ordered",
        "delivery",
    )
    ordering = (
        "user",
        "product",
        "number",
        "date_ordered",
        "delivery",
    )  # 해당 애트리뷰트들로 순서
    list_filter = ("delivery",)  # 해당 애트리뷰트로 filtering 가능
