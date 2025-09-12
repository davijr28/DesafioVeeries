from django.db import models

# Create your models here.
class Navio(models.Model):
    data_chegada = models.DateTimeField()
    volume = models.CharField(max_length=100) #mudar para DecimalField
    produto = models.CharField(max_length=200)
    sentido = models.CharField(max_length=50)
    porto = models.CharField(max_length=100)
