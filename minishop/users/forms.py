from django import forms

from . import models

# 로그인 폼
class LoginForm(forms.Form):
    email = forms.EmailField()  # 이메일
    password = forms.CharField(widget=forms.PasswordInput)  # 패스워드

    # 폼 커스텀
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

    # 폼 확인
    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)  # 해당 email을 가진 유저를 가져옴
            if user.check_password(password):  # 비밀번호가 같다면
                return self.cleaned_data
            else:  # 틀리면 메세지
                self.add_error("password", forms.ValidationError("비밀번호가 틀립니다."))
        except models.User.DoesNotExist:  # 해당 email을 가진 유저가 없다면
            self.add_error("email", forms.ValidationError("이메일이 존재하지 않습니다."))


# 날짜 뷰 형식 바꿔주는 클래스
class XYZ_DateInput(forms.DateInput):

    input_type = "date"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"  # 연도-월-일 순
        # kwargs["format"] = "%d-%m-%Y"
        super().__init__(**kwargs)


# 회원가입 폼
class SignUpForm(forms.ModelForm):

    """Sign Up Form Definition"""

    class Meta:
        model = models.User  # 생성할 인스턴스가 있는 테이블
        fields = (  # 사용자가 입력할 필드
            "email",
            "nickname",
            "gender",
            "birth",
            "mobile",
        )
        widgets = {  # 생일 입력방식
            "birth": XYZ_DateInput(format=["%Y-%m-%d"]),
        }

    password = forms.CharField(widget=forms.PasswordInput)  # 비밀번호 입력 필드
    password1 = forms.CharField(widget=forms.PasswordInput)  # 비밀번호 확인 입력 필드

    # email 데이터 가져옴
    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)  # 이미 user 테이블에 해당하는 email이 있다면
            raise forms.ValidationError("이미 존재하는 이메일입니다.", code="existing_user")
        except models.User.DoesNotExist:
            return email

    # 비밀번호 확인
    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password != password1:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        else:
            return password

    # 저장
    def save(self, *arg, **kwargs):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        user.set_password(password)  # 비밀번호는 그대로 저장하지 않고 암호화해서 저장
        user.save()

    # 폼 필드 커스텀
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields["email"].widget.attrs = {
            "type": "email",
            "class": "form-control",
            "id": "emailInput",
            "value": "",
            "placeholder": "name@example.com",
        }

        self.fields["password"].widget.attrs = {
            "type": "password",
            "class": "form-control",
            "id": "floatingPassword",
            "placeholder": "qwerty1234",
        }
        self.fields["password1"].widget.attrs = {
            "type": "password",
            "class": "form-control",
            "id": "floatingPassword1",
            "placeholder": "qwerty1234",
        }
        self.fields["nickname"].widget.attrs = {
            "class": "form-control",
            "id": "nicknameInput",
            "placeholder": "DBJOIN",
        }
        self.fields["gender"].widget.attrs = {
            "class": "form-select",
            "id": "genderInput",
        }
        self.fields["birth"].widget.attrs = {
            "class": "form-control",
            "id": "birthInput",
            "placeholder": "2000-01-01",
        }
        self.fields["mobile"].widget.attrs = {
            "class": "form-control",
            "id": "mobileInput",
            "placeholder": "01234567890",
        }
