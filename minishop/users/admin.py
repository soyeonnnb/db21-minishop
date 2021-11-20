from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):  # Admin 페이지에 User 테이블 추가

    """User Admin Definition"""

    fieldsets = (  # User 애트리뷰트들 분류
        (
            "Basic Info",  # 기본 정보
            {
                "fields": (
                    "email",
                    "nickname",
                    "gender",
                    "birth",
                    "mobile",
                )
            },
        ),
        (
            "Others",  # 추가 정보
            {
                "fields": (
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    list_display = (  # 메인 화면에서 해당 애트리뷰트들 보이기
        "email",
        "nickname",
        "mobile",
        "is_staff",
    )
    ordering = ("email", "nickname", "is_staff")  # 해당 애트리뷰트들로 순서
    list_filter = ("is_staff",)  # 해당 애트리뷰트로 filtering 가능
