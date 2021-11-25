from django.db import models
from django.db.models.deletion import SET_NULL
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Review(models.Model):

    """Review Model Definition"""

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="reviews"
    )
    order = models.ForeignKey(
        "orders.Order", on_delete=SET_NULL, related_name="reviews", null=True
    )
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
