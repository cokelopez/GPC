from django.test import TestCase
from .models import Pagos, Gasto

# Create your tests here.


class TestModels(TestCase):

    def test_pagos_absolute_url(self):
        pagos = pagos()
        pagos.carro = 1
        pagos.pago = 2300
        pagos.fecha = '2020-03-19'
        pagos.semana = '2020-W11'

        self.assertEqual(pagos.get_absolute_url(), 'pagos')

    def test_gasto_absolute_url(self):
        gasto = gasto()
        gasto.monto = 500
        gasto.iva = True
        gasto.fecha = '2020-03-19'
        gasto.gasto = 2
        gasto.carro = 1

        self.assertEqual(gasto.get_absolute_url(), 'gasto')
