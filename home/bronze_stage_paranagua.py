import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from home.models import Navio
from datetime import datetime


class Command(BaseCommand):
    help = "Importa dados de navios esperados do Porto de Paranaguá"

    def handle(self, *args, **kwargs):
        url = "https://www.appaweb.appa.pr.gov.br/appaweb/pesquisa.aspx?WCI=relLineUpRetroativo"
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")

        tabelas = soup.find_all(
            "table", class_="table table-bordered table-striped table-hover"
        )

        for tabela in tabelas:
            linhas = tabela.find_all("tr")
            for linha in linhas:
                colunas = linha.find_all("td")
                if not colunas:
                    continue
                primeira_coluna = colunas[0].text.strip()

                if tabela.find('th',colspan="22").text == 'ATRACADOS':
                    if primeira_coluna.isdigit():
                        data_chegada_raw = colunas[14].text.strip()
                        volume = colunas[18].text.strip()
                        produto = colunas[12].text.strip()
                        sentido = colunas[9].text.strip()
                    else:
                        data_chegada_raw = colunas[6].text.strip()
                        volume = colunas[10].text.strip()
                        produto = colunas[4].text.strip()
                        sentido = colunas[1].text.strip()
                elif tabela.find('th',colspan="22").text == 'PROGRAMADOS':
                    if primeira_coluna.isdigit():
                        data_chegada_raw = colunas[15].text.strip()
                        volume = colunas[19].text.strip()
                        produto = colunas[14].text.strip()
                        sentido = colunas[11].text.strip()
                    else:
                        data_chegada_raw = colunas[5].text.strip()
                        volume = colunas[9].text.strip()
                        produto = colunas[4].text.strip()
                        sentido = colunas[1].text.strip()
                elif tabela.find('th',colspan="22").text == 'AO LARGO':
                    if primeira_coluna.isdigit():
                        data_chegada_raw = colunas[13].text.strip()
                        volume = colunas[16].text.strip()
                        produto = colunas[11].text.strip()
                        sentido = colunas[8].text.strip()
                    else:
                        data_chegada_raw = colunas[5].text.strip()
                        volume = colunas[8].text.strip()
                        produto = colunas[3].text.strip()
                        sentido = colunas[0].text.strip()
                elif tabela.find('th',colspan="22").text == 'DESPACHADOS':
                    if primeira_coluna.isdigit():
                        data_chegada_raw = colunas[13].text.strip()
                        volume = colunas[17].text.strip()
                        produto = colunas[12].text.strip()
                        sentido = colunas[9].text.strip()
                else:
                    data_chegada_raw = colunas[5].text.strip()
                    volume = colunas[9].text.strip()
                    produto = colunas[4].text.strip()
                    sentido = colunas[1].text.strip()
                
                try:            
                    data_chegada = datetime.strptime(data_chegada_raw, "%d/%m/%Y %H:%M")
                except ValueError:
                    data_chegada = None

                Navio.objects.create(
                    data_chegada=data_chegada,
                    volume=volume,
                    produto=produto,
                    sentido=sentido,
                    porto="Porto de Paranaguá",
                )

        self.stdout.write(self.style.SUCCESS("Importação concluída!"))
