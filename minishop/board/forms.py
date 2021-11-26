from django import forms
from . import models


#  FAQ POST 를 생성하는 폼 클래스
class CreateFAQPostForm(forms.ModelForm):
    class Meta:
        model = models.FAQPost
        fields = ["title", "body", "photo"]

    def __init__(self, *args, **kwargs):
        super(CreateFAQPostForm, self).__init__(*args, **kwargs)

        self.fields["title"].widget.attrs = {
            "class": "form-control",
            "id": "floatingInput",
        }

        self.fields["body"].widget.attrs = {
            "type": "text",
            "class": "form-control",
            "id": "floatingPassword",
        }
        self.fields["photo"].widget.attrs = {
            "class": "form-control",
            "id": "fileInput",
        }


#  FAQ 답변을 생성하는 폼 클래스
class CreateFAQCommentForm(forms.ModelForm):
    class Meta:
        model = models.FAQComment
        fields = ["comment"]

    def __init__(self, *args, **kwargs):
        super(CreateFAQCommentForm, self).__init__(*args, **kwargs)

        self.fields["comment"].widget.attrs = {
            "type": "text",
            "class": "form-control",
            "placeholder": "답변을 입력해주세요",
        }
