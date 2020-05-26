from django.test import TestCase, Client
from django.urls import reverse
from carros.models import *
from carros.views import *
import json


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.conductor = Conductores.objects.create(
            nombres='Jorge',
            apellidos='López',
            edad=38,
            telefono=8114903913
        )

        self.propietario = Propietarios.objects.create(
            nombres='Angelica',
            apellidos='Vela',
            telefono=8110613928
        )

        self.carro = Carros.objects.create(
            nombre='Carro prueba',
            marca='Nissan',
            modelo='Versa',
            year='2016',
            placa='STP8384',
            color='Plata',
            propietario=self.propietario,
            is_active=1


        )
        self.renta = Renta.objects.create(
            nombre='prueba',
            renta=1500,
            carro=self.carro,
        )

    def test_project_Conductores_list(self):

        # response = self.client.post(
        #     '/login/', {'username': 'jorge.lopez', 'password': 'jolo1815'})
        record = Conductores.objects.get(nombres='Jorge', apellidos='López')
        response = self.client.get(reverse('conductores'))
        self.assertEqual(str(record), 'Jorge López')
        self.assertEqual(response.status_code, 302)
