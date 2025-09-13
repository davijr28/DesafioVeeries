from django.shortcuts import render
from django.db.models import Sum
from home.models import NavioSilver
from django.urls import reverse


def home(request):
    return render(request, "home.html")


def gold_volume_diario(request):
    dados = (
        NavioSilver.objects.values("data_chegada", "produto", "porto", "sentido")
        .annotate(volume_total=Sum("volume"))
        .order_by("-data_chegada", "porto", "produto", "sentido")
    )
    return render(request, "app.html", {"dados": dados})
