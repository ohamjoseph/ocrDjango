from django import forms
from django.contrib.auth.models import User
from django.forms import FileInput, CharField

from ocr.models import UploadPDF


class FormUploadPDF(forms.ModelForm):
    class Meta:
        model = UploadPDF
        fields = ['name']
        widgets = {
            'name': FileInput(attrs={'class':"form-control",'type':"file",'id':"formFileDisabled"}),
        }

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username','email','password']

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'type':"text",'tabindex':"1",'class':"form-control",'placeholder':"Username"}
        )
    )
    password = forms.CharField(widget=forms.TextInput(
        attrs={'type':"password",'tabindex':"2",'class':"form-control",'placeholder':"password"}
        )
    )

class SearchForm(forms.Form):
    searchTerm = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control', 'type':'search'}))