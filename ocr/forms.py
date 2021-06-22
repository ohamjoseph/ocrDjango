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
    password_confirm = forms.CharField(widget=forms.TextInput(
        attrs={'type': "password", 'tabindex': "2", 'class': "form-control", 'placeholder': "Confirmer mot de passe"}
    )
    )
    class Meta:
        model = User
        fields = ['username','email','password']

        widgets = {

            'username': forms.TextInput(attrs={'class': "form-control", 'type': "text",'tabindex':'1', 'placeholder': "Nom d'utilsateur"}),
            'email': forms.TextInput(attrs={ 'class': "form-control", 'type': "text",'tabindex':'1', 'placeholder': "Adresse mail"}),
            'password': forms.TextInput(attrs={'class': "form-control", 'type': "password", 'tabindex':'2', 'placeholder': "Mot de pass"}),

        }

    def clean(self):
        super().clean()
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('password_confirm')
        if p1 != p2:
            raise forms.ValidationError(
                ' les mots de passe ne correspondent pas'
            )


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'type':"text",'tabindex':"1",'class':"form-control",'placeholder':"Nom d'utilisateur"}
        )
    )
    password = forms.CharField(widget=forms.TextInput(
        attrs={'type':"password",'tabindex':"2",'class':"form-control",'placeholder':"Mot de passe"}
        )
    )

class SearchForm(forms.Form):
    searchterm = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control', 'type':'search'}))