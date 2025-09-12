import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from home.models import Navio
from datetime import datetime


class Command(BaseCommand):
    help = "Importa dados de navios esperados do Porto de Santos"

    def handle(self, *args, **kwargs):
        url = "https://www.portodesantos.com.br/informacoes-operacionais/operacoes-portuarias/navegacao-e-movimento-de-navios/navios-esperados-carga"
        page = requests.get(url, verify=False)
        soup = BeautifulSoup(page.text, "html.parser")

        tabelas = soup.find_all("div", style="overflow-x:auto;margin-bottom:20px;")

        for tabela in tabelas:
            linhas = tabela.find_all("tr", class_="text-center")

            for linha in linhas:
                colunas = linha.find_all("td")
                if not colunas:
                    continue

                data_chegada_raw = colunas[4].text.strip()
                volume = colunas[9].text.strip()
                produto = colunas[8].text.strip()
                sentido = colunas[7].text.strip()

                try:
                    data_chegada = datetime.strptime(data_chegada_raw, "%d/%m/%Y %H:%M")
                except ValueError:
                    data_chegada = None

                Navio.objects.create(
                    data_chegada=data_chegada,
                    volume=volume,
                    produto=produto,
                    sentido=sentido,
                    porto="Porto de Santos",
                )

        self.stdout.write(self.style.SUCCESS("Importação concluída!"))
