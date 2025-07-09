import django_filters

from pet.models import Pet


class CaseInsensitiveInFilter(django_filters.BaseInFilter):
    def filter(self, qs, value):
        if value:
            # Приводимо все до нижнього регістру
            value = [v.lower() for v in value if isinstance(v, str)]
            # Застосовуємо фільтр
            lookup = f"{self.field_name}__in"
            return qs.filter(**{lookup: value})
        return qs


class PetFilter(django_filters.FilterSet):

    weight__gt = django_filters.NumberFilter(
        field_name="weight", lookup_expr="gt"
    )
    weight__lt = django_filters.NumberFilter(
        field_name="weight", lookup_expr="lt"
    )
    weight__gte = django_filters.NumberFilter(
        field_name="weight", lookup_expr="gte"
    )
    weight__lte = django_filters.NumberFilter(
        field_name="weight", lookup_expr="lte"
    )
    age__gt = django_filters.NumberFilter(
        field_name="age", lookup_expr="gt", label="age__gt"
    )
    age__lt = django_filters.NumberFilter(field_name="age", lookup_expr="lt")
    age__gte = django_filters.NumberFilter(field_name="age", lookup_expr="gte")
    age__lte = django_filters.NumberFilter(field_name="age", lookup_expr="lte")

    date_after = django_filters.DateFilter(
        field_name="date_created",
        lookup_expr="gte",
        label="Created on or after",
    )
    date_before = django_filters.DateFilter(
        field_name="date_created",
        lookup_expr="lte",
        label="Created on or before",
    )
    pet_type = CaseInsensitiveInFilter(field_name="pet_type", lookup_expr="in")
    coloration = CaseInsensitiveInFilter(
        field_name="coloration", lookup_expr="in"
    )
    breed = CaseInsensitiveInFilter(field_name="breed", lookup_expr="in")
    name = django_filters.CharFilter(
        field_name="name", lookup_expr="icontains"
    )
    owner = CaseInsensitiveInFilter(
        field_name="owner", lookup_expr="icontains"
    )

    class Meta:
        model = Pet
        fields = [
            "id",
            "name",
            "pet_type",
            "age",
            "breed",
            "sex",
            "coloration",
            "weight",
            "is_sterilized",
            "owner",
            "weight",
            "date_created",
            "age__gt",
        ]
