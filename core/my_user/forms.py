from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import AbstractUserClass


class RegisterForm(UserCreationForm):
    class Meta:
        model = AbstractUserClass
        fields = ['username', 'password1', 'password2']


class AuthForm(AuthenticationForm):
    class Meta:
        model = AbstractUserClass
        fields = ['username', 'password']
