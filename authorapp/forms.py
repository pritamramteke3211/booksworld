from django import forms
from django.forms import widgets
from .models import *


        
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
