
from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework import routers


urlpatterns = [

    path('clients/list', clients_list, name='clients-list'),


    path('clients/details', clients_details, name='clients-details'),
    path('clients/details/<client_id>', clients_details, name='clients-details'),
    path('clients/details/<client_id>/<periodStart>', clients_details, name='clients-details'),
    path('clients/details/<client_id>/<periodStart>/<periodEnd>', clients_details, name='clients-details'),


    path('clients/returns', clients_returns, name='clients-returns'),
    path('clients/returns/<client_id>', clients_returns, name='clients-returns'),
    path('clients/returns/<client_id>/<periodStart>', clients_returns, name='clients-returns'),
    path('clients/returns/<client_id>/<periodStart>/<periodEnd>', clients_returns, name='clients-returns'),
    
]