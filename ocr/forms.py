from django import forms
from django.forms import FileInput

from ocr.models import UploadPDF


class FormUploadPDF(forms.ModelForm):
    class Meta:
        model = UploadPDF
        fields = ['name']
        widgets = {
            'name': FileInput(attrs={'class':"form-control",'type':"file",'id':"formFileDisabled"}),
        }


class SearchForm(forms.Form):
    searchTerm = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control', 'type':'search'}))