import django_filters
from django_filters import CharFilter
from django_filters import DateFilter
from django import forms 


from .models import *

class Passenger_details_filter(django_filters.FilterSet):
    borading = CharFilter(field_name='borading',lookup_expr='icontains')
    class Meta:
        model = CustomerDetails
        fields = ['borading']