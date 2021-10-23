from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import widgets
from .models import *


class SignUp(UserCreationForm):
    ## if you want to edit password field which only inherit from UserCreationForm
    password2 = forms.CharField(label='Confirm Password (again)', widget=forms.PasswordInput)
    # group = forms.CharField(label='Select_Group')
    
    class  Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email']
        labels = {'email': 'Email'}
        widgets = {'username':forms.TextInput(attrs={'class':'form-control'})}


        
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name','author','genre','cover','pdf','summary']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'author':forms.TextInput(attrs={'class':'form-control'}),
            'genre':forms.TextInput(attrs={'class':'form-control'}),
            # 'cover':forms.ImageField(),
            # 'pdf':forms.FileField(),
            'summary':forms.Textarea(attrs={'class':'form-control'}),
            
            }
