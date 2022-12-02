from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class signupform(UserCreationForm):
    email=forms.CharField(max_length=255,required=True,widget=forms.EmailInput)

    class Meta:
        model=User
        fields={'username','email','password1','password2'}
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }