from django import forms
from . import models


class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = [
            "number",
            "method",
            "address",
        ]

    def __init__(self, *args, **kwargs):
        super(CreateOrderForm, self).__init__(*args, **kwargs)
