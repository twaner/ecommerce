__author__ = 'taiowawaner'

from django import forms


# Forms

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
