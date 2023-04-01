from django.db import models
from django_filters import CharFilter, FilterSet, NumericRangeFilter

from .models import Apartment


class ApartmentFilter(FilterSet):

    # The JSON Field did not work directly, until it is declared here separately
    size = CharFilter(field_name="specifications__size", lookup_expr="exact")
    bedrooms = CharFilter(field_name="specifications__bedrooms", lookup_expr="exact")
    toilets = CharFilter(field_name="specifications__toilets", lookup_expr="exact")
    bathrooms = CharFilter(field_name="specifications__bathrooms", lookup_expr="exact")
    price = NumericRangeFilter(field_name="price", lookup_expr="range")

    # Same with this fields, Probably because of the look_up
    # With this setuo, one can simplify the name of the attribute passed in the query parameter
    address = CharFilter(field_name="address", lookup_expr="icontains")
    agent_id = CharFilter(field_name="agent_id", lookup_expr="exact")

    class Meta:
        model = Apartment
        fields = {
            "category": ["exact"],
            "_type": ["exact"],
            "state": ["exact"],
            "property_ref": ["exact"],
        }

    def filter_queryset(self, queryset):
        # Override the query to allow it search for Comma Separated values
        for name, value in self.form.cleaned_data.items():
            # Check if value contains comma

            if value is not None and "," in value:
                # Split value by comma and convert to list
                values = value.split(",")
                # Apply OR operator to filter queryset with multiple values passed
                queryset = queryset.filter(**{f"{name}__in": values})
            else:
                queryset = self.filters[name].filter(queryset, value)

            assert isinstance(
                queryset, models.QuerySet
            ), "Expected '%s.%s' to return a QuerySet, but got a %s instead." % (
                type(self).__name__,
                name,
                type(queryset).__name__,
            )
        return queryset


# ? Note
# * icontains does not work well with CSV probably because it later needs to add __in to the lookup, exact works just fine
