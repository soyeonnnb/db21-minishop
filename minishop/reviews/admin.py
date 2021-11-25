from django.contrib import admin

from . import models

# Register your models here.
@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):

    """Review Admin"""

    fieldsets = (
        (
            None,
            {
                "fields": ("user", "order", "review", "rating"),
            },
        ),
    )

    list_display = ("user", "order", "review", "created_at", "rating")

    ordering = ("-created_at", "user", "order", "rating")

    list_filter = ("rating",)
