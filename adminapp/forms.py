from django import forms
from .models import *
from django.contrib.auth.models import User,Group
from django.contrib.auth.forms import UserCreationForm

CHOICES = [('Author','Author'),('Reader','Reader')]

class ReaderSignupForm(UserCreationForm):
        name = forms.CharField(max_length=50,label='Your Name',widget=forms.TextInput())
        position= forms.CharField(label='Position', widget=forms.Select(choices=CHOICES))
        class  Meta:
            model = User
            fields = ['username','email']
            labels = {'email': 'Email','position':'Position'}
            widgets = {
                'username': forms.TextInput(), ## You can add attrs inside Input and class inside attrs dictionary
                'email': forms.EmailInput(), 
                
            }
        field_order=['username','name','email','position','password1','password2']

# class LoginForm(AuthenticationForm):
#     class Meta:
#         model = User
#         fields = ['username','password']