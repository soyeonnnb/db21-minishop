from django.db import models
from django.core.validators import MinValueValidator
from django.db.models.fields import related

# Order 테이블
class Order(models.Model):

    """Order Model Definition"""

    # method는 select 할 수 있어, 이 셋 중 하나의 값을 가짐
    METHOD_CASH = "cash"
    METHOD_CARD = "card"
    METHOD_PAY = "pay"
    METHOD_CHOICES = (
        (METHOD_CASH, "Cash"),
        (METHOD_CARD, "Card"),
        (METHOD_PAY, "Pay"),
    )

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="orders"
    )  # 주문자 애트리뷰트 foreign key 가 사라지면 해당 객체도 삭제
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE, related_name="orders"
    )  # 상품 애트리뷰트 foreign key 가 사라지면 해당 객체도 삭제
    number = models.IntegerField(
        default=1, validators=[MinValueValidator(1)]
    )  # 주문 수량 애트리뷰트
    date_ordered = models.DateTimeField(auto_now_add=True)  # 주문 날짜 애트리뷰트
    method = models.CharField(
        max_length=4, choices=METHOD_CHOICES, default=METHOD_CASH
    )  # 결제방법 애트리뷰트
    address = models.TextField(null=False)  # 주소 애트리뷰트
    delivery = models.BooleanField(default=False)  # 배송 여부 애트리뷰트

    def __str__(self):
        return f"{self.user} - {self.product}"

    # 해당 테이블을 fk로 하는 reviews를 가져오는 함수
    def get_reviews(self):
        return self.reviews.all()

    # 해당 테이블을 fk로 하는 reviews가 있는지 확인해주는 함수
    def has_reviews(self):
        all_reviews = self.reviews.all()
        return len(all_reviews) > 0

    # AWS RDS 사용
    class Meta:
        managed = False
        db_table = "order"  # MySql에서 사용하는 테이블 이름
