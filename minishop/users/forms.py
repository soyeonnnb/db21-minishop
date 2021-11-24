from django import forms
from django.contrib.auth.forms import (
    UserChangeForm,
    AuthenticationForm,
)
from . import models


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields["email"].widget.attrs = {
            "type": "email",
            "class": "form-control",
            "id": "floatingInput",
        }

        self.fields["password"].widget.attrs = {
            "type": "password",
            "class": "form-control",
            "id": "floatingPassword",
        }

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("비밀번호가 틀립니다."))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("이메일이 존재하지 않습니다."))


# 날짜 뷰 형식 바꿔주는 클래스
class XYZ_DateInput(forms.DateInput):

    input_type = "date"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"  # 연도-월-일 순
        # kwargs["format"] = "%d-%m-%Y"
        super().__init__(**kwargs)


class SignUpForm(forms.ModelForm):

    """Sign Up Form Definition"""

    class Meta:
        model = models.User
        fields = (
            "email",
            "nickname",
            "gender",
            "birth",
            "mobile",
        )
        widgets = {
            "birth": XYZ_DateInput(format=["%Y-%m-%d"]),
        }

    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError("이미 존재하는 이메일입니다.", code="existing_user")
        except models.User.DoesNotExist:
            return email

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password != password1:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        else:
            return password

    def save(self, *arg, **kwargs):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        user.set_password(password)
        user.save()
