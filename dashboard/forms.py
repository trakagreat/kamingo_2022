from .models import ServiceModel
from django import forms
from django.forms import ModelForm


class EditServiceForm(ModelForm):
    class Meta:
        model = ServiceModel
        fields = '__all__'
        exclude = ('review', 'slug', 'address', 'description', 'user', 'image')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'multiple': ""}),
            'service_provider_name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),

        }

