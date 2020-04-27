import django_filters
from .models import Pagos, Conductores
from django.db.models import Q


class ConductoresFilter(django_filters.FilterSet):

    buscar = django_filters.CharFilter(
        method='filtro_nombres')

    class Meta:
        model = Conductores
        fields = ['buscar']

    def filtro_nombres(self, queryset, name, value):
        return Conductores.objects.filter(
            Q(nombres__icontains=value) | Q(apellidos__icontains=value))


class PagosFilter(django_filters.FilterSet):
    semana = django_filters.ModelChoiceFilter(field_name='semana',
                                              queryset=Pagos.objects.order_by('semana').distinct('semana'))

    class Meta:
        model = Pagos
        fields = ['semana', ]
