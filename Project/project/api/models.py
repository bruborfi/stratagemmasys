from django.db import models

# Create your models here.

class Movimiento(models.Model):
    operation_date = models.DateField()
    rut = models.CharField(max_length=50)
    account_name = models.CharField(max_length=50)
    nemo_name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    desc = models.CharField(max_length=50)
    price = models.FloatField()
    quantity = models.FloatField()
    total = models.FloatField()

class Saldos(models.Model):
    date = models.DateField(auto_now=True)
    rut = models.CharField(max_length=50)
    account = models.CharField(max_length=50)
    total = models.FloatField()
    exchange_rate = models.FloatField()
    currency = models.CharField(max_length=50)
