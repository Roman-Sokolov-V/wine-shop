import django_filters

from pet.models import Pet


class PetFilter(django_filters.FilterSet):
    weight__gt = django_filters.NumberFilter(field_name="weight", lookup_expr="gt")
    weight__lt = django_filters.NumberFilter(field_name="weight", lookup_expr="lt")
    weight__gte = django_filters.NumberFilter(field_name="weight",
                                             lookup_expr="gte")
    weight__lte = django_filters.NumberFilter(field_name="weight",
                                             lookup_expr="lte")
    age__gt = django_filters.NumberFilter(field_name="weight",
                                             lookup_expr="gt")
    age__lt = django_filters.NumberFilter(field_name="weight",
                                             lookup_expr="lt")
    age__gte = django_filters.NumberFilter(field_name="weight",
                                              lookup_expr="gte")
    age__lte = django_filters.NumberFilter(field_name="weight",
                                              lookup_expr="lte")
    age__gte = django_filters.NumberFilter(field_name="weight",
                                           lookup_expr="gte")
    age__lte = django_filters.NumberFilter(field_name="weight",
                                           lookup_expr="lte")
    date_after = django_filters.DateFilter(
        field_name="date_created",
        lookup_expr="gte",
        label="Created on or after"
    )
    date_before = django_filters.DateFilter(
        field_name="date_created",
        lookup_expr="lte",
        label="Created on or before"
    )

    class Meta:
        model = Pet
        fields = ["weight", "age", "date_created"]