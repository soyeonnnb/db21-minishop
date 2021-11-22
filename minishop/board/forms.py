from django import forms
from . import models


class CreateFAQPostForm(forms.ModelForm):
    class Meta:
        model = models.FAQPost
        fields = ["title", "body", "photo"]


class CreateFAQCommentForm(forms.ModelForm):
    class Meta:
        model = models.FAQComment
        fields = ["comment"]

    def __init__(self, *args, **kwargs):
        super(CreateFAQCommentForm, self).__init__(*args, **kwargs)

        self.fields["comment"].widget.attrs = {
            "class": "form-control",
            "placeholder": "답변을 입력해주세요",
        }
