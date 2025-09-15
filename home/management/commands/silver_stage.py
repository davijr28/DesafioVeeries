import re
from decimal import Decimal, InvalidOperation
from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from home.models import NavioBronze, NavioSilver


# Função para limpar o valor de volume
def limpar_volume(volume_str: str):
    total = Decimal("0.00")
    # Divide a string caso haja mais de 1 valor com base no delimitador "<br/>"
    partes = volume_str.split("<br/>")

    # Encontra todos os valores numéricos
    for parte in partes:
        numeros = re.findall(r"[\d.,]+", parte)
        if numeros:
            # Ajusta o formato do número
            numero = numeros[0].replace(".", "").replace(",", ".")
            try:
                total += Decimal(numero)  # Tenta somar ao total
            except InvalidOperation:
                continue  # Ignora caso não seja possível
    return total.quantize(
        Decimal("0.01")  # Retorna o valor arredondado para 2 casas decimais
    )


# Função para limpar e converter o formato da data
def limpar_data(data_str):
    if not data_str:
        return None

    # Tenta converter string para datetime com diferentes formatos
    for fmt in ("%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M", "%d/%m/%Y"):
        try:
            dt = datetime.strptime(data_str.strip(), fmt)
            return make_aware(dt)  # Retorna a data convertida para o fuso horário
        except ValueError:
            continue  # Se não for compatível, tenta o próximo
    return None  # Retorna None se não conseguir converter


# Função para padronizar o sentido do navio
def limpar_sentido(sentido_str):
    sentido_str = sentido_str.strip()
    if sentido_str in ["Imp", "DESC"]:
        return "Importação"
    elif sentido_str in ["Exp", "EMB"]:
        return "Exportação"
    elif sentido_str in ["Imp/Exp", "EMBDESC"]:
        return "Importação/Exportação"


# Função para tratar o nome extraído do produto
def limpar_produto(produto_str: str) -> str:

    # Verifica se a parte da string está vazia e retorna a parte não vazia
    try:
        if produto_str.split("<br/>")[0].strip() == "":
            return produto_str.split("<br/>")[1].strip()
        elif produto_str.split("<br/>")[1].strip() == "":
            return produto_str.split("<br/>")[0].strip()
        # Verifica se os nomes são iguais, caso contrário, retorna os dois
        elif (
            produto_str.split("<br/>")[0].strip()
            != produto_str.split("<br/>")[1].strip()
        ):
            return f"{produto_str.split('<br/>')[0].strip()}, {produto_str.split('<br/>')[1].strip()}"
        else:
            return produto_str.split("<br/>")[0].strip()
    except IndexError:
        return produto_str.split("<br/>")[0].strip()


# Comando para transformar dados da tabela Bronze em Silver
class Command(BaseCommand):
    help = "Transforma dados da tabela Bronze em Silver"

    def handle(self, *args, **options):
        # Itera sobre todos os objetos na tabela Bronze
        for navio in NavioBronze.objects.all():
            # Para cada objeto NavioBronze, cria um novo objeto NavioSilver com os dados limpos, caso já não exista
            NavioSilver.objects.get_or_create(
                data_chegada=limpar_data(navio.data_chegada),
                volume=limpar_volume(navio.volume),
                produto=limpar_produto(navio.produto),
                sentido=limpar_sentido(navio.sentido),
                porto=navio.porto.strip(),
            )

        # Exibe mensagem de sucesso no terminal
        self.stdout.write(
            self.style.SUCCESS("Transformação Bronze -> Silver concluída!")
        )
