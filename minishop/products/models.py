from django.db import models


class ProductCategory(models.Model):

    """Custom Product Category Model"""

    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Product Categories"


# Create your models here.
class Product(models.Model):

    """Custom Product Model"""

    name = models.CharField(max_length=100)
    price = models.IntegerField()
    inventory = models.IntegerField()
    description = models.TextField()
    categories = models.ManyToManyField(
        "ProductCategory", related_name="products", blank=True
    )
    photo = models.ImageField(blank=True, null=True, upload_to="product_photo")
    discountinue = models.BooleanField(default=False)
