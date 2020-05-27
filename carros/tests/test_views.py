from django.test import TestCase, Client
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from carros.models import *
from carros.views import *
import json


class TestViews(TestCase):

    def setUp(self):
        password = 'mypassword'
        my_admin = User.objects.create_superuser(
            'myuser', 'myemail@test.com', password)

        self.client = Client()
        # self.loginuser = User.objects.create_user(
        #     username='testuser1',
        #     password='jolo1815')

        self.agregarconductor_url = reverse('conductor_new')
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

    # def test_carros_Conductores_list(self):

    #     record = Conductores.objects.get(nombres='Jorge', apellidos='López')
    #     response = self.client.get(reverse('conductores'))
    #     self.assertEqual(str(record), 'Jorge López')
    #     self.assertEqual(response.status_code, 302)

    def test_carros_Conductores_nuevo(self):

        login = self.client.login(
            username='myuser',
            password='mypassword'
        )

        response = self.client.post(reverse('conductor_new'), {
            'nombres': 'Juan',
            'apellidos': 'Garza',
            'edad': 30,
            'telefono': 8114903914
        })

        self.assertEqual(Conductores.objects.last().nombres, 'Juan')
