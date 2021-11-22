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


class UpdateOrderForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = [
            "number",
            "method",
            "address",
        ]
