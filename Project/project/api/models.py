from django.db import models

# OBS:
# -No fue posible descargar a la tabla cartera de inversion y se decidió no inventar.
# -Se ha comentado la normalización dado que se ha determinado que la api debe funcionar con la base de datos entregada


# class Cliente(models.Model):
#     name = models.CharField(max_length=50)
#     rut = models.CharField(max_length=50)
#     email = models.EmailField(max_length=254)


# class Account(models.Model):
#     name = models.CharField(max_length=50)
#     cliente = models.ForeignKey(Cliente, related_name='accounts', on_delete=models.CASCADE)


class Movimiento(models.Model):
    operation_date = models.DateField()
    rut = models.CharField(max_length=50)
    account_name = models.CharField(max_length=50) #account = models.ForeignKey(Account, related_name='movimientos', on_delete=models.CASCADE)
    nemo_name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    desc = models.CharField(max_length=50)
    price = models.FloatField()
    quantity = models.FloatField()
    total = models.FloatField()


class Saldos(models.Model):
    date = models.DateField(auto_now=True)
    rut = models.CharField(max_length=50) 
    account = models.CharField(max_length=50) #account = models.ForeignKey(Account, related_name='saldos', on_delete=models.CASCADE)
    total = models.FloatField()
    exchange_rate = models.FloatField()
    currency = models.CharField(max_length=50)
