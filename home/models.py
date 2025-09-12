from django.db import models


class NavioBronze(models.Model):
    data_chegada = models.CharField(null=True, blank=True, max_length=100)
    volume = models.CharField(max_length=100)
    produto = models.CharField(max_length=200)
    sentido = models.CharField(max_length=50)
    porto = models.CharField(max_length=50)
    data_importacao = models.DateTimeField(auto_now_add=True)


class NavioSilver(models.Model):
    data_chegada = models.DateTimeField(null=True, blank=True)
    volume = models.DecimalField(max_digits=50, decimal_places=2)
    produto = models.CharField(max_length=200)
    sentido = models.CharField(max_length=50)
    porto = models.CharField(max_length=50)
    data_importacao = models.DateTimeField(auto_now_add=True)
