from django.contrib import admin
from . import models

# Product Category Admin Page
@admin.register(models.ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):  # Admin 페이지에 상품 카테고리 추가

    """Product Category Admin Definition"""

    list_display = ("name", "used_by")  # 메인화면에서 이름과 사용 횟수(해당 카테고리에 해당하는 상품 수) 보이기

    def used_by(self, obj):
        return obj.products.count()


# Product Category Admin Page
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):  # Admin 페이지에 상품 추가

    """Product Admin Definition"""

    fieldsets = (  # 상품 애트리뷰트들 분류
        (
            "Basic Info",
            {"fields": ("name", "description", "price", "category", "photo")},
        ),
        (
            "Inventory",
            {
                "fields": ("inventory", "discontinue"),
            },
        ),
    )
    ordering = ("name", "price", "inventory", "created_at")  # 이름, 가격, 재고 수로 순서
    list_display = (  # 메인 화면에 보이는 애트리뷰트
        "name",
        "price",
        "inventory",
        "discontinue",
        "created_at",
    )
    list_filter = (  # 해당 애트리뷰트들로 filtering 가능
        "category",
        "discontinue",
    )
