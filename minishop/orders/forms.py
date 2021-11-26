from django import forms
from . import models

# 주문을 생성해주는 폼
class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = models.Order  # 해당 테이블의 인스턴스 생성
        fields = [  # 사용자가 입력할 애트리뷰트
            "number",
            "method",
            "address",
        ]

    # 폼 커스텀
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


# 주문을 수정해주는 폼
class UpdateOrderForm(forms.ModelForm):
    class Meta:
        model = models.Order  # 해당 테이블의 인스턴스가 수정됨
        fields = [  # 수정할 애트리뷰트
            "number",
            "method",
            "address",
        ]

    # 폼 커스텀
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
