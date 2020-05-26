from django.test import SimpleTestCase
from django.urls import resolve, reverse
from carros.views import *
# HomeView, GraficaBarras_Pagos, ConductoresListView, ConductoresCreate, ConductoresUpdate, ConductoresDelete, PropietariosListView, PropietariosCreate, PropietariosUpdate, PropietariosDelete,CarrosListView,CarrosCreate, CarrosUpdate, CarrosUpdate


class TestUrls(SimpleTestCase):
    def test_url_home(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func.view_class, HomeView)

    def test_url_grafica(self):
        url = reverse('pagos-grafica')
        self.assertEquals(resolve(url).func.view_class, GraficaBarras_Pagos)

    def test_url_conductores(self):
        url = reverse('conductores')
        self.assertEquals(resolve(url).func.view_class, ConductoresListView)

    def test_url_conductores_create(self):
        url = reverse('conductor_new')
        self.assertEquals(resolve(url).func.view_class, ConductoresCreate)

    def test_url_conductores_update(self):
        url = reverse('conductor_edit', args=[1])
        self.assertEquals(resolve(url).func.view_class, ConductoresUpdate)

    def test_url_conductores_delete(self):
        url = reverse('conductor_borrar', args=[1])
        self.assertEquals(resolve(url).func.view_class, ConductoresDelete)

    def test_url_propietarios(self):
        url = reverse('propietarios')
        self.assertEquals(resolve(url).func.view_class, PropietariosListView)

    def test_url_propietarios_create(self):
        url = reverse('propietario_new')
        self.assertEquals(resolve(url).func.view_class, PropietariosCreate)

    def test_url_propietarios_update(self):
        url = reverse('propietario_edit', args=[1])
        self.assertEquals(resolve(url).func.view_class, PropietariosUpdate)

    def test_url_propietarios_delete(self):
        url = reverse('propietario_borrar', args=[1])
        self.assertEquals(resolve(url).func.view_class, PropietariosDelete)

    def test_url_carros(self):
        url = reverse('carros')
        self.assertEquals(resolve(url).func.view_class, CarrosListView)

    def test_url_carros_create(self):
        url = reverse('carros_new')
        self.assertEquals(resolve(url).func.view_class, CarrosCreate)

    def test_url_carros_update(self):
        url = reverse('carros_edit', args=[1])
        self.assertEquals(resolve(url).func.view_class, CarrosUpdate)

    def test_url_insurance(self):
        url = reverse('polizas')
        self.assertEquals(resolve(url).func.view_class, PolizasListView)

    def test_url_insurance_create(self):
        url = reverse('poliza_new')
        self.assertEquals(resolve(url).func.view_class, PolizaCreate)

    def test_url_insurance_update(self):
        url = reverse('poliza_edit', args=[1])
        self.assertEquals(resolve(url).func.view_class, PolizaUpdate)

    def test_url_insurance_delete(self):
        url = reverse('poliza_borrar', args=[1])
        self.assertEquals(resolve(url).func.view_class, PolizaDelete)

    def test_url_expenses(self):
        url = reverse('gasto')
        self.assertEquals(resolve(url).func.view_class, GastoListView)

    def test_url_expenses_create(self):
        url = reverse('gasto_new')
        self.assertEquals(resolve(url).func.view_class, GastoCreate)

    def test_url_expenses_update(self):
        url = reverse('gasto_edit', args=[1])
        self.assertEquals(resolve(url).func.view_class, GastoUpdate)

    def test_url_expenses_delete(self):
        url = reverse('gasto_borrar', args=[1])
        self.assertEquals(resolve(url).func.view_class, GastoDelete)

    def test_url_payments(self):
        url = reverse('pagos')
        self.assertEquals(resolve(url).func.view_class, PagosListView)

    def test_url_payments_addtoexistingweek(self):
        url = reverse('pago_existente', args=[1, 1])
        self.assertEquals(resolve(url).func.view_class, AgregarPagoSemana)

    def test_url_payments_create(self):
        url = reverse('pagos_new')
        self.assertEquals(resolve(url).func.view_class, PagosCreate)

    def test_url_payments_create_bycarrandweek(self):
        url = reverse('pagos_bycar', args=[1, 1])
        self.assertEquals(resolve(url).func.view_class, PagosDetailView)

    def test_url_payments_delete(self):
        url = reverse('pagos_borrar', args=[1])
        self.assertEquals(resolve(url).func.view_class, PagosDelete)
