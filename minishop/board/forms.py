from django import forms
from . import models


class CreateFAQPostForm(forms.ModelForm):
    class Meta:
        model = models.FAQPost
        fields = ["title", "body", "photo"]
