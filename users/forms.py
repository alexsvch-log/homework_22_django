from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


# 1. Форма регистрации нового пользователя
class UserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        # Поля, которые пользователь будет заполнять при регистрации (Email и пароль идут по умолчанию)
        fields = ("email", "phone", "country", "avatar")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем красивую стилизацию Bootstrap для всех полей формы
        for _, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'


# 2. Форма авторизации (Входа)
class UserLoginForm(AuthenticationForm):
    # Переопределяем поле ввода логина на Email
    username = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'example@mail.ru'
    }), label="Электронная почта")

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Пароль'
    }), label="Пароль")

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'phone', 'country', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'

