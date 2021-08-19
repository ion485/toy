from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import EmailField

from user.models import User

class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'name')

class LoginForm(AuthenticationForm):
    username = EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))