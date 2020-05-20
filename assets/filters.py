import django_filters
from po.models import Po
from .models import Assets
from psycopg2.extras import DateRange
from django_filters import DateFromToRangeFilter, ModelChoiceFilter
from django.forms.widgets import TextInput


class DateExactRangeWidget(DateFromToRangeFilter):
    """Date widget to help filter by *_start and *_end."""
    suffixes = ['start', 'end']


class DateExactRangeField(DateFromToRangeFilter):
    widget = DateExactRangeWidget

    def compress(self, data_list):
        if data_list:
            start_date, stop_date = data_list
            return DateRange(start_date, stop_date)


class AssetsFilter(django_filters.FilterSet):
    procurement_date = DateExactRangeField(label='Procurement Date Range',
                                           widget=django_filters.widgets.RangeWidget(
                                               attrs={'placeholder': 'yyyy/mm/dd'}))
    branch__Name = django_filters.CharFilter(
        lookup_expr='icontains', label='Branch', widget=TextInput(attrs={'placeholder': 'Branch'}))
    product_type = django_filters.CharFilter(
        lookup_expr='icontains', label='Product Type', widget=TextInput(attrs={'placeholder': 'Product Type'}))
    status = django_filters.CharFilter(
        lookup_expr='icontains', label='Status', widget=TextInput(attrs={'placeholder': 'Status'}))


    class Meta:
        model = Assets
        fields = {
            'product_type',
            'branch__Name',
            'procurement_date',
            'status'
        }



class UrAssetsFilter(django_filters.FilterSet):

    product_type = django_filters.CharFilter(
        lookup_expr='icontains', label='Product Type', widget=TextInput(attrs={'placeholder': 'Product Type'}))
    po__po_number = django_filters.CharFilter(
        lookup_expr='icontains', label='Po Number', widget=TextInput(attrs={'placeholder': 'Po Number'}))
    vendor_name = django_filters.CharFilter(
        lookup_expr='icontains', label='Vendor Name', widget=TextInput(attrs={'placeholder': 'Vendor Name'}))

    class Meta:
        model = Assets
        fields = {
            'product_type',
            'po__po_number',
            'vendor_name'
        }
