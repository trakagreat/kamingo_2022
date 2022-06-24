from django.forms import ModelForm
from .models import ServiceModel, ImageModel, Address
from django import forms


class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        exclude = ('city',)
        widgets = {
            'address_line1': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line2': forms.TextInput(attrs={'class': 'form-control'}),
            'pin_code': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ServiceForm(ModelForm):
    class Meta:
        model = ServiceModel
        fields = '__all__'
        exclude = ('review', 'slug', 'address','description','user','image')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control',
                                                  'type': 'tel',
                                                  'pattern':"^\d{10}$"  }),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            # 'image': forms.FileInput(attrs={'class': 'form-control', 'multiple':""}),
            'service_provider_name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),

        }


class ImageForm(ModelForm):
    class Meta:
        model = ImageModel
        fields = '__all__'

# class ReviewForm(ModelForm):
#     rating = forms.Select()
#     class Meta:
#         model = ReviewModel
#         fields = ['rating', 'content']
#         labels = {
#             'rating': 'rating',
#             'content': 'review'
#         }
#         widgets = {
#             'content': forms.Textarea(attrs={
#                 'class': 'form-control',
#             })
#         }
