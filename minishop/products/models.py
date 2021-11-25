from django.db import models
from django.urls import reverse
from django.shortcuts import redirect
from django.core.validators import MinValueValidator


class ProductCategory(models.Model):

    """Product Category Model Definition"""

    name = models.CharField(max_length=50)  # 이름 애트리뷰트

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Product Categories"


def product_directory_path(instance, filename):
    return "faq_product/product_{}/{}".format(instance.id, filename)


# Create your models here.
class Product(models.Model):

    """Product Model Definition"""

    name = models.CharField(max_length=100)  # 이름 애트리뷰트
    price = models.IntegerField(validators=[MinValueValidator(1)])  # 가격 애트리뷰트
    inventory = models.PositiveIntegerField(
        validators=[MinValueValidator(0)]
    )  # 재고 애트리뷰트
    description = models.TextField()  # 설명 애트리뷰트
    categories = models.ForeignKey(
        "ProductCategory",
        related_name="products",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )  # 카테고리 애트리뷰트
    photo = models.ImageField(
        blank=True, null=True, upload_to=product_directory_path
    )  # 사진 애트리뷰트
    created_at = models.DateTimeField(auto_now_add=True)  # 상품 생성 날짜 애트리뷰트
    discountinue = models.BooleanField(default=False)  # 단종여부 애트리뷰트

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"pk": self.pk})

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating
            return round(all_ratings / len(all_reviews), 2)
        return 0
