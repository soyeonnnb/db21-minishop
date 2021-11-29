import random
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator

# 상품 카테고리 테이블
class ProductCategory(models.Model):

    """Product Category Model Definition"""

    name = models.CharField(max_length=50)  # 이름 애트리뷰트

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Product Categories"

        # AWS RDS 사용
        managed = False
        db_table = "category"  # MySql에서 사용하는 테이블 이름


# 상품 사진 이름 커스텀을 위한 함수
def product_directory_path(instance, filename):
    n = random.randint(1000000000, 9999999999)
    return "product/product_{}{}/{}".format(instance.id, n, filename)


# Product 테이블
class Product(models.Model):

    """Product Model Definition"""

    name = models.CharField(max_length=100)  # 이름 애트리뷰트
    price = models.IntegerField(validators=[MinValueValidator(1)])  # 가격 애트리뷰트
    inventory = models.PositiveIntegerField(
        validators=[MinValueValidator(0)]
    )  # 재고 애트리뷰트, 최소 0의 값을 가짐
    description = models.TextField()  # 설명 애트리뷰트
    category = models.ForeignKey(
        "ProductCategory",
        related_name="products",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )  # 카테고리 애트리뷰트, 앞서 만든 category 테이블의 값을 fk로 가짐
    photo = models.ImageField(
        blank=True, null=True, upload_to=product_directory_path
    )  # 사진 애트리뷰트
    created_at = models.DateTimeField(auto_now_add=True)  # 상품 생성 날짜 애트리뷰트
    discontinue = models.BooleanField(default=False)  # 단종여부 애트리뷰트

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"pk": self.pk})

    # 해당 product의 별점을 구함
    def total_rating(self):
        all_reviews = self.reviews.all()  # 해당 테이블을 fk로 가지는 reviews 테이블의 인스턴스를 가져옴
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += (
                    review.rating
                )  # review테이블의 rating 애트리뷰트의 값 만큼 all_rating에 더해줌
            return round(all_ratings / len(all_reviews), 2)
        return 0

    # AWS RDS 사용
    class Meta:
        managed = False
        db_table = "product"  # MySql에서 사용하는 테이블 이름
