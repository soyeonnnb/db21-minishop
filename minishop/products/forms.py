from django import forms

from . import models

# 상품을 생성해주는 폼
class CreateProductForm(forms.ModelForm):
    class Meta:
        model = models.Product  # 해당 테이블의 인스턴스 생성
        fields = (  # 사용자가 입력할 폼
            "name",
            "price",
            "inventory",
            "description",
            "categories",
            "photo",
        )

    # 폼 커스텀
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
