import django_filters
from django.db.models import Q
from cars.models import Car


class CarsFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_text')
    ordering = django_filters.OrderingFilter(
        fields=('price', 'created_at', 'year'),

        field_labels={
            'price': 'Цена по возрастанию',
            '-price': 'Цена по убыванию',
            'created_at': 'Сначала новые',
            '-created_at': 'Сначала старые',
            'year': 'По году выпуска',
        }
    )
    brand = django_filters.CharFilter(field_name="brand__name", lookup_expr='icontains')
    city = django_filters.CharFilter(lookup_expr='icontains')
    transmission = django_filters.CharFilter(lookup_expr='icontains')
    fuel = django_filters.CharFilter(lookup_expr='icontains')
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    year_min = django_filters.NumberFilter(field_name='year', lookup_expr='gte')
    year_max = django_filters.NumberFilter(field_name='year', lookup_expr='lte')

    def filter_by_text(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(Q(brand__name__icontains=value) |
                               Q(model__icontains=value) |
                               Q(description__icontains=value))

    class Meta:
        model = Car
        fields = ['ordering', 'search','brand', 'city', 'transmission',
                  'fuel', 'price_min', 'price_max', 'year_min', 'year_max']