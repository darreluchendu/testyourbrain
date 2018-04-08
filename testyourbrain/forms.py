from django import forms
from django.contrib.auth.models import User

from testyourbrain.models import UserProfile, GameSession


class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')


class NewSession(forms.ModelForm):
    name=forms.CharField()

    class Meta:
        model=GameSession
        fields=('name',)