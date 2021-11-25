from django import forms

from . import models


class CreateReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
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
