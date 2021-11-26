from django.db import models

# 찜 하기 Table
class Wish(models.Model):

    """Wish Model Definition"""

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE
    )  # 찜하기 버튼을 누른 user를 fk로 받음
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE
    )  # 찜하기 된 product를 fk로 받음
    added_date = models.DateTimeField(auto_now_add=True)  # 찜 한 날짜

    def __str__(self):
        return f"{self.user} - {self.product}"

    # AWS RDS 사용
    class Meta:
        managed = False
        db_table = "wish"  # MySql에서 사용하는 테이블 이름
