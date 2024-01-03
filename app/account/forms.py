from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput


User = get_user_model()


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].label = "Ваш e-mail"
        self.fields["email"].required = True
        self.fields["username"].help_text = "Используй латинские буквы"
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists() and len(email) > 254:
            raise forms.ValidationError(
                """Пользователь с таким e-mail уже существует или
                                         длина e-mail превышает 254 символов"""
            )
        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=TextInput(attrs={"placeholder": "Логин", "class": "form-control"})
    )
    password = forms.CharField(
        widget=PasswordInput(attrs={"placeholder": "Пароль", "class": "form-control"})
    )


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].help_text = "Ваш E-mail адрес"
        self.fields["email"].required = True

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if (
            User.objects.filter(email=email).exclude(id=self.instance.id).exists()
            and len(email) > 254
        ):
            raise forms.ValidationError(
                """Данный e-mail уже используется или
                                         длина e-mail превышает 254 символов"""
            )
        return email

    class Meta:
        model = User
        fields = ("username", "email")
        exclude = ("password1", "password2")
