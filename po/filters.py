import django_filters
from po.models import Po
from psycopg2.extras import DateRange
from django_filters import DateFromToRangeFilter
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


class PoFilter(django_filters.FilterSet):
    created_at = DateExactRangeField(label='Created Date Range',
                                     widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'yyyy/mm/dd'}))
    po_number = django_filters.CharFilter(lookup_expr='icontains', label='Po Number', widget=TextInput(attrs={'placeholder': 'Po_Number'}))
    #
    # CHOICES = (
    #     ('ascending', 'Ascending'),
    #     ('descending', 'Descending')
    # )
    # ordering = django_filters.ChoiceFilter(label='Ordering', choices=CHOICES, method='filter_by_order')

    class Meta:
        model = Po
        fields = {
            'created_at',
            'po_number',
            'approved_by',
            'processed'
        }
    #
    # def filter_by_order(self, queryset, name, value):
    #     expression = 'procurement_date' if value == 'ascending' else '-procurement_date'
    #     return queryset.order_by(expression)
