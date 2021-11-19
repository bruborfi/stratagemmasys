from rest_framework import viewsets, status
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum, CharField, Value, F

# Create your views here.

# Nº 1 --> /api/clients/list
@api_view(['GET'])
def clients_list(request):
    
    LIMIT_DAY = datetime.date.today() - datetime.timedelta(days=30)

    clients = Movimiento.objects.filter(operation_date__gte=LIMIT_DAY).values('rut', 'account_name').distinct('rut')

    return Response(clients)


#funcion de validacion compartida entre las siguientes dos vistas funcionales
def validate_api_params(client_id=None, periodStart=None, periodEnd=None):
    request_errors = {}

    # validando client_id
    if client_id == None:
        request_errors["client_id"]=['Campo obligatorio']
    else:
        try:
            int(client_id)
        except:
            request_errors["client_id"]=['Debe ser un número']



    # validando periodStart
    if periodStart == None:
        request_errors["periodStart"] = ['Campo obligatorio']
        periodStart_valid = None
    else:
        try:
            periodStart_valid = datetime.datetime.strptime(periodStart, '%Y-%m-%d')
        except:
            periodStart_valid = None
            request_errors["periodStart"] = ['Debe ser una fecha valida en formato %Y-%m-%d']


    # validando periodEnd
    if periodEnd == None:
        request_errors["periodEnd"] = ['Campo obligatorio']
        periodEnd_valid = None
    else:
        try:
            periodEnd_valid = datetime.datetime.strptime(periodEnd, '%Y-%m-%d')
        except:
            periodEnd_valid = None
            request_errors["periodEnd"] = ['Debe ser una fecha valida en formato %Y-%m-%d']

    # validando congruencia entre principio y fin
    if periodEnd_valid and periodStart_valid and periodEnd_valid < periodStart_valid:
        request_errors["periodStart_periodEnd"] = ['periodStart debe ser menor a PeriodEnd.']


    return request_errors


# Nº 2 --> /api/clients/details/{client_id}/{periodStart}/{periodEnd}
@api_view(['GET'])
def clients_details(request, client_id=None, periodStart=None, periodEnd=None):

    validate = validate_api_params(client_id, periodStart, periodEnd)
    if len(validate.keys()) > 0:
        return Response(validate, status=status.HTTP_400_BAD_REQUEST)

    response_errors = {}

    client_data = Movimiento.objects.filter(rut=client_id).values('account_name').distinct('rut')
    saldos_periodStart = Saldos.objects.filter(rut=client_id, date=periodStart)
    saldos_periodEnd = Saldos.objects.filter(rut=client_id, date=periodEnd)

    patrimonio_inicial = saldos_periodStart.aggregate(Sum('total'))['total__sum']
    patrimonio_final= saldos_periodEnd.aggregate(Sum('total'))['total__sum']

    if len(client_data) == 0:
        response_errors["client_id"] = ['No hay clientes asociados a este rut.']
        return Response(response_errors, status=status.HTTP_400_BAD_REQUEST)

    if len(saldos_periodStart) == 0:
        response_errors["periodStart"] = ['No hay saldos registrados para este período.']
    
    if len(saldos_periodEnd) == 0:
        response_errors["periodEnd"] = ['No hay saldos registrados para este período.']

    if len(response_errors.keys()) > 0:
        return Response(response_errors, status=status.HTTP_400_BAD_REQUEST)


    response = {}
    response['rut'] = client_id
    response['nombre'] = client_data[0]["account_name"]
    response['email'] = None #información no entregada
    response['cuentas'] = Saldos.objects.filter(rut=client_id).values('account').distinct('account')
    response['patrimonio_inicial'] = patrimonio_inicial #Falta sumar instrumentos en cartera #Tabla cartera inversion inaccesible
    response['patrimonio_final'] = patrimonio_final #Falta sumar instrumentos en cartera #Tabla cartera inversion inaccesible
    response['rentabilidad_cartera'] = patrimonio_final - patrimonio_inicial  #Falta dividir por la inversion #Tabla cartera inversion inaccesible
    response['cartera_inversion_periodo'] = None #Tabla cartera inaccesible
    response['movimientos_periodo'] = Movimiento.objects.filter(rut=client_id, operation_date__gte=periodStart, operation_date__lte=periodEnd).values('operation_date', 'nemo_name', 'code', 'desc', 'price', 'quantity', 'total')
    response['caja_periodo'] = Saldos.objects.filter(rut=client_id, date__gte=periodStart, date__lte=periodEnd).values('date', 'account', 'total', 'exchange_rate', 'currency')
    
    return Response(response)

    


# Nº 3 --> /api/clients/returns/{client_id}/{periodStart}/{periodEnd}
@api_view(['GET'])
def clients_returns(request, client_id=None, periodStart=None, periodEnd=None):

    validate = validate_api_params(client_id, periodStart, periodEnd)
    if len(validate.keys()) > 0:
        return Response(validate, status=status.HTTP_400_BAD_REQUEST)

    response = Movimiento.objects.all().values('rut', 'account_name').distinct('rut').annotate(
        rentabilidad=Value(
            float(Saldos.objects.filter(rut=F('rut'), date=periodStart).aggregate(Sum('total'))['total__sum'] - Saldos.objects.filter(rut=F('rut'), date=periodEnd).aggregate(Sum('total'))['total__sum']) # Tabla cartera inacesible # Se debe dividir este valor por la inversion asociada a la cartera del cliente en el periodo
            )
        )
    
    
    
    return Response(response)