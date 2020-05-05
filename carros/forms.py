from django import forms
from django.core.exceptions import ValidationError
from .models import Conductores, Propietarios, Carros, Polizas, Gasto, Pagos, Renta, Inactividad
import datetime


class PostConductores(forms.ModelForm):
    class Meta:
        model = Conductores
        fields = ('nombres', 'apellidos', 'telefono', 'edad', 'ine')


class EditConductores(forms.ModelForm):
    class Meta:
        model = Conductores
        fields = ('nombres', 'apellidos', 'telefono', 'edad', 'ine')


class PostPropietarios(forms.ModelForm):
    class Meta:
        model = Propietarios
        fields = ('nombres', 'apellidos', 'telefono')


class EditPropietarios(forms.ModelForm):
    class Meta:
        model = Propietarios
        fields = ('nombres', 'apellidos', 'telefono')


class PostCarros(forms.ModelForm):
    class Meta:
        model = Carros
        fields = ('nombre', 'marca', 'modelo', 'year',
                  'placa', 'color', 'conductor', 'propietario')


class EditCarros(forms.ModelForm):
    class Meta:
        model = Carros
        fields = ('nombre', 'marca', 'modelo', 'year',
                  'placa', 'color', 'conductor', 'propietario')


class PostPolizas(forms.ModelForm):
    class Meta:
        model = Polizas
        fields = ('nombre', 'numero', 'aseguradora', 'carro', 'inicio_poliza',
                  'fin_poliza', 'documento')
        widgets = {'inicio_poliza': forms.DateInput(attrs={'type': 'date'}),
                   'fin_poliza': forms.DateInput(attrs={'type': 'date'})
                   }


class EditPolizas(forms.ModelForm):
    class Meta:
        model = Polizas
        fields = ('nombre', 'numero', 'aseguradora', 'carro', 'inicio_poliza',
                  'fin_poliza', 'documento')
        widgets = {'inicio_poliza': forms.DateInput(attrs={'type': 'date'}),
                   'fin_poliza': forms.DateInput(attrs={'type': 'date'})
                   }


class PostGasto(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = ('monto', 'iva', 'fecha', 'gasto', 'carro', 'factura')
        widgets = {'fecha': forms.DateInput(attrs={'type': 'date'})
                   }


class EditGasto(forms.ModelForm):

    class Meta:
        model = Gasto
        fields = ('monto', 'iva', 'fecha', 'gasto', 'carro', 'factura')
        widgets = {'fecha': forms.DateInput(attrs={'type': 'date'})
                   }


class AgregarPagoTransaccionExistente(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.carro = kwargs.pop('carro')
        self.semana = kwargs.pop('semana')
        super(AgregarPagoTransaccionExistente, self).__init__(*args, **kwargs)

    class Meta:
        model = Pagos
        fields = ('carro', 'pago', 'fecha', 'semana', 'renta')
        widgets = {'fecha': forms.DateInput(attrs={'type': 'date'}),
                   'semana': forms.DateInput(attrs={'type': 'week'})
                   }


class PostPagos(forms.ModelForm):

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']

        if fecha > datetime.date.today():
            raise forms.ValidationError(
                'La Fecha no puede ser mayor al día de hoy')
        return fecha

    class Meta:
        model = Pagos
        fields = ('carro', 'pago', 'fecha', 'semana', 'renta', 'imagen')
        widgets = {'fecha': forms.DateInput(attrs={'type': 'date'}),
                   'semana': forms.DateInput(attrs={'type': 'week'})
                   }


class AdminInactividad(forms.ModelForm):

    def clean(self):
        clean_data = super(AdminInactividad, self).clean()
        carro = clean_data.get('carro')
        activo = Carros.objects.values_list(
            'is_active', flat=True).filter(nombre=carro)

        print(activo)
        if activo[0]:
            raise forms.ValidationError('El Auto está activo')

    class Meta:
        model = Inactividad
        fields = ('razon', 'carro', 'fecha_inicio', 'fecha_fin')


class PostPolizas(forms.ModelForm):
    class Meta:
        model = Polizas
        fields = ('nombre', 'numero', 'aseguradora', 'carro', 'inicio_poliza',
                  'fin_poliza', 'documento')
        widgets = {'inicio_poliza': forms.DateInput(attrs={'type': 'date'}),
                   'fin_poliza': forms.DateInput(attrs={'type': 'date'})
                   }
