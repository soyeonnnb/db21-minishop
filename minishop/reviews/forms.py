from django import forms

from . import models

# 리뷰 생성 폼
class CreateReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review  # 해당 테이블의 인스턴스 생성
        fields = ("review", "rating")

    def __init__(self, *args, **kwargs):
        super(CreateReviewForm, self).__init__(*args, **kwargs)

        self.fields["review"].widget.attrs = {
            "class": "form-control",
            "id": "reviewInput",
            "style": "height: 100px",
            "placeholder": "리뷰를 작성해주세요",
        }
        self.fields["rating"].widget.attrs = {
            "class": "form-control",
            "id": "ratingInput",
            "max": 5,
            "min": 1,
        }
