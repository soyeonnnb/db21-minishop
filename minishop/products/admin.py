from django.contrib import admin
from . import models


@admin.register(models.ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):

    """Product Category Admin Definition"""

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.products.count()

    pass


# Register your models here.
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):

    """Product Admin Definition"""

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "name",
                    "description",
                    "price",
                    "categories",
                )
            },
        ),
        (
            "Inventory",
            {
                "fields": ("inventory", "discountinue"),
            },
        ),
    )
    ordering = ("name", "price", "inventory")
    list_display = (
        "name",
        "price",
        "inventory",
        "discountinue",
    )
    list_filter = (
        "categories",
        "discountinue",
    )
