from django import forms

from . import models


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = (
            "name",
            "price",
            "inventory",
            "description",
            "categories",
            "photo",
        )

    def __init__(self, *args, **kwargs):
        super(CreateProductForm, self).__init__(*args, **kwargs)

        self.fields["name"].widget.attrs = {
            "class": "form-control",
            "id": "numberInput",
            "type": "number",
        }

        self.fields["price"].widget.attrs = {
            "class": "form-select",
            "id": "priceInput",
            "min": 0,
        }

        self.fields["inventory"].widget.attrs = {
            "class": "form-control",
            "id": "inventoryInput",
            "min": 0,
        }
        self.fields["description"].widget.attrs = {
            "class": "form-control",
            "id": "descriptionInput",
        }
        self.fields["categories"].widget.attrs = {
            "class": "form-select",
            "id": "categoriesInput",
        }
        self.fields["photo"].widget.attrs = {
            "class": "form-control",
            "id": "photoInput",
        }
