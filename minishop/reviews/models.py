from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Review 테이블
class Review(models.Model):

    """Review Model Definition"""

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="reviews"
    )  # 리뷰 작성자 애트리뷰트 foreign key 가 사라지면 해당 객체도 삭제
    order = models.ForeignKey(
        "orders.Order", on_delete=models.CASCADE, related_name="reviews"
    )  # 리뷰가 작성되는 주문 애트리뷰트 foreign key 가 사라지면 해당 객체도 삭제
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="reviews",
    )  # 리뷰가 작성되는 상품 애트리뷰트 foreign key 가 사라지면 해당 객체도 삭제
    review = models.TextField()  # 리뷰 내용 애트리뷰트
    created_at = models.DateTimeField(auto_now_add=True)  # 리뷰 작성 날짜 애트리뷰트
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )  # 리뷰 rating 애트리뷰트, 최소 1, 최대 5의 정수값을 가짐
