from django.db import models


# 사진 저장이름 수정 함수
def faq_directory_path(instance, filename):
    import os
    from random import randint
    from django.utils.timezone import now

    filename_base, filename_ext = os.path.splitext(filename)

    return "faq_photo/{}/{}" % (
        # instance.id,
        now().strftime("%Y%m%d") + "_" + str(randint(100, 999)),
        filename,
    )


# FAQPost 모델(DB에서는 테이블)
class FAQPost(models.Model):

    """FAQ Post Model Definition"""

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE
    )  # 유저 애트리뷰트, foreign key로서 삭제시 cascade로 함께 삭제
    title = models.CharField(max_length=255)  # 제목 애트리뷰트, 최대길이 255자
    body = models.TextField()  # 본문 애트리뷰트
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 날짜, 자동으로 추가됨
    updated_at = models.DateTimeField(auto_now=True)  # 수정 날짜, 자동으로 수정됨
    photo = models.ImageField(
        blank=True, null=True, upload_to=faq_directory_path
    )  # 사진 애트리뷰트

    # 해당 데이터베이스는 self.title 로 보임
    def __str__(self):
        return self.title

    # 해당 instance를 foreign키로 하는 comments가 있는지 확인해주는 함수
    def has_comments(self):
        all_comments = self.comments.all()
        return len(all_comments) > 0

    # 사진을 원하는 이름으로 저장하기 위해 만든 함수.
    def save(self, *args, **kwargs):
        if self.id is None:
            temp_image = self.photo
            self.photo = None
            super().save(*args, **kwargs)
            self.photo = temp_image
            super().save(*args, **kwargs)

    # AWS RDS 사용
    class Meta:
        managed = False
        db_table = "post"  # MySql에서 사용하는 테이블 이름


# FAQ 답변 테이블
class FAQComment(models.Model):

    """FAQ Comment Definition"""

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE
    )  # 유저 애트리뷰트, foreign key로서 삭제시 cascade로 함께 삭제
    post = models.ForeignKey(
        FAQPost, on_delete=models.CASCADE, related_name="comments"
    )  # post 애트리뷰트, foreign key로서 삭제시 cascade로 함께 삭제
    comment = models.TextField()  # 내용 애트리뷰트
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 날짜 애트리뷰트, 생성 시 자동 입력
    updated_at = models.DateTimeField(auto_now=True)  # 수정 날짜 애트리뷰트, 수정 시 자동 입력

    # AWS RDS 사용
    class Meta:
        managed = False
        db_table = "comment"  # MySql에서 사용하는 테이블 이름
