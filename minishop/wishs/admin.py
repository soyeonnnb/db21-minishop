from django.contrib import admin

from . import models

# Wish Admin Custom
@admin.register(models.Wish)
class WishAdmin(admin.ModelAdmin):

    fieldsets = (
        (
            None,
            {
                "fields": ("user", "product"),
            },
        ),
    )
    list_display = ("user", "product", "added_date")  # 메인 화면에서 해당 애트리뷰트들 보이기
    ordering = ("user", "product", "added_date")  # 해당 애트리뷰트들로 순서
