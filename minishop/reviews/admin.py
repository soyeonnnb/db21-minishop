from django.contrib import admin

from . import models

# Review Admin 커스텀. 다른 테이블과 형식 동일
@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):

    """Review Admin Definition"""

    fieldsets = (
        (
            None,
            {
                "fields": ("user", "order", "review", "rating"),
            },
        ),
    )

    list_display = (
        "user",
        "order",
        "review",
        "created_at",
        "rating",
    )  # 메인 화면에서 해당 애트리뷰트들 보이기

    ordering = ("-created_at", "user", "order", "rating")  # 해당 애트리뷰트들로 순서

    list_filter = ("rating",)  # 해당 애트리뷰트로 filtering 가능
