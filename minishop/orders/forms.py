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

        self.fields["number"].widget.attrs = {
            "class": "form-control",
            "id": "numberInput",
            "type": "number",
            "min": 1,
        }

        self.fields["method"].widget.attrs = {
            "class": "form-select",
            "id": "methodInput",
        }

        self.fields["address"].widget.attrs = {
            "class": "form-control",
            "id": "addressInput",
        }


class UpdateOrderForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = [
            "number",
            "method",
            "address",
        ]

    def __init__(self, *args, **kwargs):
        super(UpdateOrderForm, self).__init__(*args, **kwargs)

        self.fields["number"].widget.attrs = {
            "class": "form-control",
            "id": "numberInput",
            "type": "number",
            "min": 1,
        }

        self.fields["method"].widget.attrs = {
            "class": "form-select",
            "id": "methodInput",
        }

        self.fields["address"].widget.attrs = {
            "class": "form-control",
            "id": "addressInput",
        }
