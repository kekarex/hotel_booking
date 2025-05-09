from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'password1', 'password2')

class ProfileForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone')
