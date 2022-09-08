

from xml.dom.minidom import Attr
import django_filters
from .models import ServiceModel
from django.forms.widgets import TextInput


class ServiceFilter(django_filters.FilterSet):

   
    address__city = django_filters.CharFilter(label='City',lookup_expr='icontains',widget=TextInput(attrs={
        'placeholder':'City'
    }))
    address__pin_code = django_filters.CharFilter(widget=TextInput(attrs={
        'placeholder':'Pincode'
    }))

    class Meta:
        model = ServiceModel
        fields = ['category','address__city' , 'address__pin_code']

        url = 'serviceapp:front-page'


        




        


