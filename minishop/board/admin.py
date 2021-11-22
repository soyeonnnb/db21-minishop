from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.FAQPost)
class FAQPostAdmin(admin.ModelAdmin):

    """Custom FAQPost Admin"""

    fieldsets = (  # User 애트리뷰트들 분류
        (
            "Basic Info",  # 기본 정보
            {
                "fields": (
                    "user",
                    "title",
                    "body",
                    "photo",
                )
            },
        ),
    )
    list_display = (  # 메인 화면에서 해당 애트리뷰트들 보이기
        "user",
        "title",
        "created_at",
        "updated_at",
    )
    ordering = (
        "title",
        "created_at",
    )  # 해당 애트리뷰트들로 순서


@admin.register(models.FAQComment)
class FAQCommentAdmin(admin.ModelAdmin):

    """Custom FAQComment Admin"""

    fieldsets = (  # User 애트리뷰트들 분류
        (
            "Basic Info",  # 기본 정보
            {
                "fields": (
                    "user",
                    "post",
                    "comment",
                )
            },
        ),
    )
    list_display = (  # 메인 화면에서 해당 애트리뷰트들 보이기
        "user",
        "post",
        "comment",
        "created_at",
        "updated_at",
    )
    ordering = (
        "user",
        "post",
        "created_at",
    )
