from unicodedata import name
import django_filters
from .models import ServiceModel


class ServiceFilter(django_filters.FilterSet):
    address__city = django_filters.CharFilter(label='City',lookup_expr='icontains')
    class Meta:
        model = ServiceModel
        fields = ['category','address__city']


