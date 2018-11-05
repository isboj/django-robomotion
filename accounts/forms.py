from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm

from .models import User


# TODO: なぜか効かない
class CustomAuthForm(AuthenticationForm):
    """
    AuthenticationFromをオーバーライドして、placeholderを設定する
    urls.pyで設定していることも確認すること。
    """
    username = forms.CharField(widget=TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Password'}))


class UserCreationForm(BaseUserCreationForm):
    """
    Userのカスタムモデルにしたため、定義している
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ('username', 'email')
