import re
from decimal import Decimal, InvalidOperation
from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from home.models import NavioBronze, NavioSilver


def limpar_volume(volume_str: str):
    total = Decimal("0.00")
    partes = volume_str.split("<br/>")
    for parte in partes:
        numeros = re.findall(r"[\d.,]+", parte)
        if numeros:
            numero = numeros[0].replace(".", "").replace(",", ".")
            try:
                total += Decimal(numero)
            except InvalidOperation:
                continue
    return total.quantize(Decimal("0.01"))


def limpar_data(data_str):
    if not data_str:
        return None
    for fmt in ("%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M", "%d/%m/%Y"):
        try:
            dt = datetime.strptime(data_str.strip(), fmt)
            return make_aware(dt)
        except ValueError:
            continue
    return None


def limpar_sentido(sentido_str):
    sentido_str = sentido_str.strip()
    if sentido_str in ["Imp", "DESC"]:
        return "Importação"
    elif sentido_str in ["Exp", "EMB"]:
        return "Exportação"
    elif sentido_str in ["Imp/Exp", "EMBDESC"]:
        return "Importação/Exportação"


def limpar_produto(produto_str: str) -> str:
    if produto_str.split("<br/>")[0].strip() == "":
        return produto_str.split("<br/>")[1]
    else:
        return produto_str.split("<br/>")[0].strip()


class Command(BaseCommand):
    help = "Transforma dados da tabela Bronze em Silver"

    def handle(self, *args, **options):
        for navio in NavioBronze.objects.all():
            NavioSilver.objects.get_or_create(
                data_chegada=limpar_data(navio.data_chegada),
                volume=limpar_volume(navio.volume),
                produto=limpar_produto(navio.produto),
                sentido=limpar_sentido(navio.sentido),
                porto=navio.porto.strip(),
            )
        self.stdout.write(
            self.style.SUCCESS("Transformação Bronze -> Silver concluída!")
        )
