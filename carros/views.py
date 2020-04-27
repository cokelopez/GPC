import os
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from decimal import *
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.db.models.functions import Coalesce
from django.db import connection
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.views import View
from django_tables2 import SingleTableView, SingleTableMixin
from django_filters.views import FilterView
from .filters import ConductoresFilter, PagosFilter
from django.db.models import Sum, Count, Case, When
from .models import Conductores, Carros, Polizas, Propietarios, TipoGasto, Renta, Gasto, Pagos
from .tables import ConductoresTable, PropietariosTable, CarrosTable, PolizasTable, GastosTable, PagosTable, PagosDetailTable
from .forms import PostConductores, EditConductores, PostPropietarios, EditPropietarios, PostCarros, EditCarros, PostPolizas, EditPolizas, PostGasto, EditGasto, AgregarPagoTransaccionExistente, PostPagos

# Create your views here.


# def index(request):
#     return render(request, 'index.html')


# def conductores(request):
#     return render(request, 'AC/conductores_list.html')


# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail
# from django.core.mail import send_mail

# send_mail('This is the title of the email',
#           'This is the message you want to send',
#           'cokelopez@gmail.com',
#           [
#               'cokelopez@gmail.com',  # add more emails to this list of you want to
#           ]
#           )


class LogoutView(TemplateView):
    template_name = "logout.html"


class UserLogged(View):

    def user(self, request):
        username = None
        if request.user.is_authenticated():
            username = request.user.username


class HomeView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    context_object_name = 'home'
    template_name = 'home.html'
    model = Carros

    def semana_anterior(self, hoy):
        today = hoy
        weekday = today.weekday()
        start_delta = datetime.timedelta(days=weekday, weeks=1)
        lunes = today - start_delta
        domingo = lunes + datetime.timedelta(days=6)
        format_lunes = lunes.strftime('%d-%m-%Y')
        format_domingo = domingo.strftime('%d-%m-%Y')
        semanapasada = lunes.strftime('%Y-%W')
        return semanapasada, format_lunes, format_domingo, lunes, domingo

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['estatusactivos'] = Carros.objects.aggregate(
            activos=Count(Case(When(is_active=True, then=1))))
        context['estatusinactivos'] = Carros.objects.aggregate(
            inactivos=Count(Case(When(is_active=False, then=1))))
        context['totaldecarros'] = Carros.objects.all()
        hoy = datetime.date.today()
        semanapasada, format_lunes, format_domingo, lunes, domingo = self.semana_anterior(
            hoy)
        context['semana'] = semanapasada
        context['inicio_semana'] = format_lunes
        context['fin_semana'] = format_domingo
        context['pagos'] = Pagos.objects.filter(fecha__range=[lunes, domingo]).aggregate(
            total=Coalesce(Sum('pago'), 0))['total']
        context['gastos'] = Gasto.objects.filter(fecha__range=[lunes, domingo]).aggregate(
            total=Coalesce(Sum('monto'), 0))['total']
        return context


class GraficaBarras_Pagos(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        labels = []
        data1 = []
        data2 = []

        # today = datetime.date.today()

        # queryset = Pagos.objects.all().filter(fecha__month=today.month).order_by().values(
        #     'semana').annotate(PagoTotal=Sum('pago'), GastoTotal=Sum('carro__gasto__monto'))
        # queryset1 = Pagos.objects.all().filter(fecha__month=today.month).order_by(
        # ).values('semana').annotate(PagoTotal=Sum('pago'))
        # queryset2 = Gasto.objects.all().filter(fecha__month=today.month).order_by(
        # ).values('semana').annotate(GastoTotal=Sum('monto'))
        cursor = connection.cursor()
        cursor.execute("Select * from(SELECT semana, 'gasto' as tipo, SUM(monto) as monto FROM public.carros_gasto Group by semana Union all Select semana, 'pago' as tipo, SUM(pago) as monto From public.carros_pagos Group by semana) as Montos order by tipo, semana")

        def dictfetchall(cursor):
            columns = [col[0] for col in cursor.description]
            return [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]

        queryset = dictfetchall(cursor)

        # Remove label duplicates
        for entry in queryset:
            labels.append(entry['semana'])

        clean_labels = list(dict.fromkeys(labels))
        labelslist = set(clean_labels)
        clean_labels.sort()

        # Separate by type: gasto
        querysetgasto = []
        querysetgastosemana = []

        for entry in queryset:

            if entry['tipo'] == 'gasto' and entry['semana'] in clean_labels:
                querysetgasto.append(entry)
                querysetgastosemana.append(entry['semana'])

        # Separate by type: pago
        querysetpago = []
        querysetpagosemana = []
        for entry in queryset:
            if entry['tipo'] == 'pago' and entry['semana'] in clean_labels:
                querysetpago.append(entry)
                querysetpagosemana.append(entry['semana'])

        # get 'semanas' that are not in gastos and the indexes
        indexes = labelslist.difference(querysetgastosemana)
        gastos_indexes = list(indexes)
        gastos_indexes.sort()

        # get the index position of the 'semanas' that are missing
        if len(gastos_indexes) > 0:
            iterator = 0
            list_gastos_missing = []
            while iterator < len(gastos_indexes):
                try:
                    missingindexes = clean_labels.index(
                        gastos_indexes[iterator])
                    list_gastos_missing.append(missingindexes)
                    iterator += 1
                except IndexError:
                    pass

        # add the 'semanas' missing to the list
        querysetgastosemana.extend(gastos_indexes)
        querysetgastosemana.sort()

        # append to data the monto's and 0's on the missing semanas on labels
        for entry in querysetgasto:
            data2.append(entry['monto'])

        for c in list_gastos_missing:
            data2.insert(c, 0)

        # get 'semanas' that are not in pagos and the indexes
        indexes = labelslist.difference(querysetpagosemana)
        pagos_indexes = list(indexes)
        pagos_indexes.sort()

        # get the index position for 'pagos' of the 'semanas' that are missing
        if len(pagos_indexes) > 0:
            iterator = 0
            list_pagos_missing = []
            while iterator < len(pagos_indexes):
                try:
                    missingindexes = clean_labels.index(
                        pagos_indexes[iterator])
                    list_pagos_missing.append(missingindexes)
                    iterator += 1
                except IndexError:
                    pass

        # add the 'semanas' missing to the list
        querysetpagosemana.extend(pagos_indexes)
        querysetpagosemana.sort()

        # append to data the monto's and 0's on the missing semanas on labels
        for entry in querysetpago:
            data1.append(entry['monto'])

        for c in list_pagos_missing:
            data1.insert(c, 0)

        return JsonResponse(data={
            'labels': clean_labels,
            'data1': data1,
            'data2': data2,

        })


class ConductoresListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    table_class = ConductoresTable
    template_name = 'drivers.html'
    filterset_class = ConductoresFilter
    paginate_by = 10


class ConductoresCreate(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    form_class = PostConductores
    template_name = "add_driver.html"


class ConductoresUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    form_class = EditConductores
    model = Conductores
    template_name = "edit_driver.html"


class ConductoresDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    model = Conductores
    success_url = reverse_lazy('conductores')


class PropietariosListView(LoginRequiredMixin, SingleTableView):
    model = Propietarios
    table_class = PropietariosTable
    template_name = 'propietarios.html'
    paginate_by = 10


class PropietariosCreate(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    form_class = PostPropietarios
    template_name = "add_owner.html"


class PropietariosUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    form_class = EditPropietarios
    model = Propietarios
    template_name = "edit_owner.html"


class PropietariosDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    model = Propietarios
    success_url = reverse_lazy('propietarios')


class CarrosListView(LoginRequiredMixin, SingleTableView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    model = Carros
    table_class = CarrosTable
    template_name = 'carros.html'
    paginate_by = 10


class CarrosCreate(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    form_class = PostCarros
    template_name = "add_car.html"


class CarrosUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    form_class = EditCarros
    model = Carros
    template_name = "edit_car.html"


class PolizasListView(LoginRequiredMixin, SingleTableView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    model = Polizas
    table_class = PolizasTable
    template_name = 'insurance.html'
    paginate_by = 10


class PolizaCreate(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    form_class = PostPolizas
    template_name = "add_insurance.html"


class PolizaUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    form_class = EditPolizas
    model = Polizas
    template_name = "edit_insurance.html"


class PolizaDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    model = Polizas
    success_url = reverse_lazy('polizas')


class GastoListView(LoginRequiredMixin, SingleTableView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    model = Gasto
    table_class = GastosTable
    template_name = 'expenses.html'
    paginate_by = 10


class GastoCreate(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    form_class = PostGasto
    template_name = "add_expense.html"

    def form_valid(self, form):
        object = form.save(commit=False)
        object.semana = self.date_week_converter(object.fecha)
        object.save()
        return super(GastoCreate, self).form_valid(form)

    def date_week_converter(self, fecha):
        f = fecha
        # format_fecha = datetime.datetime.strptime(f, '%Y,%m,%d')
        semana_convert = f.strftime("%Y-%W")
        s = semana_convert.find('-')
        s = s + 1
        semana = semana_convert[:s] + 'W' + semana_convert[s:]
        return semana


class GastoUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    form_class = EditGasto
    model = Gasto
    template_name = "edit_expense.html"


class GastoDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    model = Gasto
    success_url = reverse_lazy('gasto')


class PagosListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    queryset = Pagos.objects.all().values(
        'carro', 'semana').annotate(PagoTotal=Sum('pago'))
    table_class = PagosTable
    template_name = 'payments.html'
    filterset_class = PagosFilter
    paginate_by = 10


class AgregarPagoSemana(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    template_name = "add_paymentexistingweek.html"
    model = Pagos
    form_class = AgregarPagoTransaccionExistente

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'semana': self.kwargs['semana'],
            'carro': self.kwargs['carro'],
        })
        return context

    def get_form_kwargs(self):
        kwargs = super(AgregarPagoSemana, self).get_form_kwargs()
        kwargs['carro'] = self.kwargs.get('carro')
        kwargs['semana'] = self.kwargs.get('semana')
        return kwargs


class PagosCreate(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    form_class = PostPagos
    template_name = "add_payment.html"

    def form_valid(self, form):
        object = form.save(commit=False)
        object.startweek, object.endweek = self.weekdatetimeconverter(
            object.semana)

        self.validation = self.pagos_validation(object.carro_id, object.pago,
                                                object.semana, object.renta_id)
        if self.validation == 1:
            object.save()
        else:
            return self.form_invalid(form)

        return super(PagosCreate, self).form_valid(form)

    def weekdatetimeconverter(self, semana):
        d = semana
        startweek = datetime.datetime.strptime(d + '-1', "%Y-W%W-%w")
        endweek = datetime.datetime.strptime(d + '-0', "%Y-W%W-%w")
        return (startweek, endweek)

    def pagos_validation(self, carro_id, pago, semana, renta_id):
        intended_payment = pago
        intended_paymentweek = semana
        intended_paymentcar = carro_id
        carrent = renta_id
        fixed_rent = self.get_renta(carrent)
        past_payments = Pagos.objects.filter(
            carro_id=intended_paymentcar, semana=intended_paymentweek).aggregate(total=Coalesce(Sum('pago'), 0))['total']

        if past_payments is None:
            validation = 1
        elif (past_payments + intended_payment) <= fixed_rent:
            validation = 1
            return validation
        else:
            validation = 0
            return validation

    def get_renta(self, carrent):
        rentadecarro = Renta.objects.filter(
            id=carrent).values_list('renta', flat=True)
        montoderenta = rentadecarro[0]

        return montoderenta


class PagosDetailView(LoginRequiredMixin, SingleTableMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    model = Pagos
    table_class = PagosDetailTable
    template_name = 'paymentsbycarandweek.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        self.object_list = self.object_list.filter(
            carro=kwargs['carro'], semana=kwargs['semana'])

        context = self.get_context_data()
        return self.render_to_response(context)


class PagosDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    model = Pagos
    success_url = reverse_lazy('pagos')


class AgregarPagoSemana(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    template_name = "add_paymentexistingweek.html"
    model = Pagos
    form_class = AgregarPagoTransaccionExistente

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'semana': self.kwargs['semana'],
            'carro': self.kwargs['carro'],
        })
        return context

    def get_form_kwargs(self):
        kwargs = super(AgregarPagoSemana, self).get_form_kwargs()
        kwargs['carro'] = self.kwargs.get('carro')
        kwargs['semana'] = self.kwargs.get('semana')
        return kwargs
