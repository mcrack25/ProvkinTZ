from django_filters import rest_framework as filters

from .models import Bill, Client, Organization


class BillFilterSet(filters.FilterSet):
    client = filters.ModelChoiceFilter(field_name='client', queryset=Client.objects.all())
    organization = filters.ModelChoiceFilter(field_name='organization', queryset=Organization.objects.all())

    class Meta:
        model = Bill
        fields = ('client', 'organization',)
