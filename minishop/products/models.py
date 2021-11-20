from django.db import models


class ProductCategory(models.Model):

    """Product Category Model Definition"""

    name = models.CharField(max_length=50)  # 이름 애트리뷰트

    class Meta:
        verbose_name_plural = "Product Categories"


# Create your models here.
class Product(models.Model):

    """Product Model Definition"""

    name = models.CharField(max_length=100)  # 이름 애트리뷰트
    price = models.IntegerField()  # 가격 애트리뷰트
    inventory = models.IntegerField()  # 재고 애트리뷰트
    description = models.TextField()  # 설명 애트리뷰트
    categories = models.ManyToManyField(
        "ProductCategory", related_name="products", blank=True
    )  # 카테고리 애트리뷰트
    photo = models.ImageField(
        blank=True, null=True, upload_to="product_photo"
    )  # 사진 애트리뷰트
    discountinue = models.BooleanField(default=False)  # 단종여부 애트리뷰트
