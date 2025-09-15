import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from home.models import NavioBronze


# Definição de comando personalizado para importar dados do porto
class Command(BaseCommand):
    help = "Importa dados de navios esperados do Porto de Paranaguá"

    def handle(self, *args, **kwargs):
        url = "https://www.appaweb.appa.pr.gov.br/appaweb/pesquisa.aspx?WCI=relLineUpRetroativo"
        page = requests.get(url)
        # Analisa o conteúdo HTML da página
        soup = BeautifulSoup(page.text, "html.parser")

        # Encontra todas as tabelas com o filtro especificado
        tabelas = soup.find_all(
            "table", class_="table table-bordered table-striped table-hover"
        )

        # Itera sobre cada tabela
        for tabela in tabelas:
            linhas = tabela.find_all("tr")

            # Itera sobre cada linha da tabela
            for linha in linhas:
                colunas = linha.find_all("td")
                if not colunas:
                    continue

                # Extrai o conteúdo da primeira coluna
                primeira_coluna = colunas[0].text.strip()
                match = False

                # Verifica o nome da tabela de dados
                if tabela.find("th", colspan="22").text == "ATRACADOS":
                    match = True

                    # Verifica se o primeiro valor é ccorrespondente ao número da linha na tabela
                    if primeira_coluna.isdigit():

                        # Coleta os dados do navio
                        data_chegada = colunas[14].text.strip()
                        volume = colunas[18].text.strip()
                        produto = colunas[12].text.strip()
                        sentido = colunas[9].text.strip()
                    else:
                        data_chegada = colunas[6].text.strip()
                        volume = colunas[10].text.strip()
                        produto = colunas[4].text.strip()
                        sentido = colunas[1].text.strip()
                elif tabela.find("th", colspan="22").text == "PROGRAMADOS":
                    match = True
                    if primeira_coluna.isdigit():
                        data_chegada = colunas[15].text.strip()
                        volume = colunas[19].text.strip()
                        produto = colunas[14].text.strip()
                        sentido = colunas[11].text.strip()
                    else:
                        data_chegada = colunas[5].text.strip()
                        volume = colunas[9].text.strip()
                        produto = colunas[4].text.strip()
                        sentido = colunas[1].text.strip()
                elif tabela.find("th", colspan="22").text == "AO LARGO":
                    match = True
                    if primeira_coluna.isdigit():
                        data_chegada = colunas[13].text.strip()
                        volume = colunas[16].text.strip()
                        produto = colunas[11].text.strip()
                        sentido = colunas[8].text.strip()
                    else:
                        data_chegada = colunas[5].text.strip()
                        volume = colunas[8].text.strip()
                        produto = colunas[3].text.strip()
                        sentido = colunas[0].text.strip()
                elif tabela.find("th", colspan="22").text == "DESPACHADOS":
                    match = True
                    if primeira_coluna.isdigit():
                        data_chegada = colunas[13].text.strip()
                        volume = colunas[17].text.strip()
                        produto = colunas[12].text.strip()
                        sentido = colunas[9].text.strip()
                    else:
                        data_chegada = colunas[5].text.strip()
                        volume = colunas[9].text.strip()
                        produto = colunas[4].text.strip()
                        sentido = colunas[1].text.strip()

                # Verifica se o nome da tabela corresponde
                if match:
                    existe = NavioBronze.objects.filter(
                        data_chegada=data_chegada,
                        volume=volume,
                        produto=produto,
                        sentido=sentido,
                        porto="Porto de Paranaguá",
                    ).exists()

                    # Verifica se o valor do objeto já está armazenado, caso contrário, cria um novo objeto
                    if not existe:
                        NavioBronze.objects.create(
                            data_chegada=data_chegada,
                            volume=volume,
                            produto=produto,
                            sentido=sentido,
                            porto="Porto de Paranaguá",
                        )

        # Exibe mensagem de sucesso no terminal
        self.stdout.write(self.style.SUCCESS("Importação concluída!"))
