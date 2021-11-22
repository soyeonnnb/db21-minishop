from django.contrib import admin

from . import models

# Register your models here.
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
    list_display = ("user", "product", "added_date")
    ordering = ("user", "product", "added_date")
