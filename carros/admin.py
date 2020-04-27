from django.contrib import admin
from .models import Conductores, Carros, Polizas, Propietarios, TipoGasto, Gasto, Renta, Pagos, Inactividad
from .forms import AdminInactividad

admin.site.register(Carros)

admin.site.register(Polizas)
admin.site.register(Propietarios)
admin.site.register(TipoGasto)


admin.site.site_header = "Administracion de Vehículos"


class GastoAdmin(admin.ModelAdmin):
    list_display = ('carro', 'gasto', 'fecha', 'monto')
    list_filter = ('carro',)


admin.site.register(Gasto, GastoAdmin)


class RentaAdmin(admin.ModelAdmin):
    list_display = ('carro', 'renta')
    list_filter = ('carro',)


admin.site.register(Renta, RentaAdmin)


class ConductoresAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'telefono')


admin.site.register(Conductores, ConductoresAdmin)


class InactividadAdmin(admin.ModelAdmin):
    form = AdminInactividad


admin.site.register(Inactividad, InactividadAdmin)


class PagosAdmin(admin.ModelAdmin):
    list_display = ('carro', 'pago', 'semana', 'renta', 'imagen')
    list_filter = ('semana', 'carro')


admin.site.register(Pagos, PagosAdmin)
