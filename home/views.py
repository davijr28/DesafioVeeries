from django.utils.timezone import now
from django.shortcuts import render
from home.models import NavioSilver

# Função para renderizar página inicial da aplicação
def home(request):
    return render(request, "home.html")


# Função para exibir o volume diário dos portos
def gold_volume_diario(request):
    
    hoje = now().astimezone().date()

    dados = NavioSilver.objects.filter(data_chegada__date__lte=hoje).order_by(
        "-data_chegada", "porto", "produto", "sentido"
    )

    santos = [d for d in dados if d.porto == "Porto de Santos"]
    paranagua = [d for d in dados if d.porto == "Porto de Paranaguá"]

    volume_santos = sum(d.volume for d in santos if d.data_chegada.date() == hoje)
    volume_paranagua = sum(d.volume for d in paranagua if d.data_chegada.date() == hoje)

    return render(
        request,
        "app.html",
        {
            "hoje": hoje,
            "santos": santos,
            "paranagua": paranagua,
            "volume_santos": volume_santos,
            "volume_paranagua": volume_paranagua,
        },
    )
