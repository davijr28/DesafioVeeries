import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from home.models import NavioBronze


# Definição de comando personalizado para importar dados do porto
class Command(BaseCommand):
    help = "Importa dados de navios esperados do Porto de Santos"

    def handle(self, *args, **kwargs):
        url = "https://www.portodesantos.com.br/informacoes-operacionais/operacoes-portuarias/navegacao-e-movimento-de-navios/navios-esperados-carga"
        page = requests.get(url, verify=False)

        # Analisa o conteúdo HTML da página
        soup = BeautifulSoup(page.text, "html.parser")

        # Encontra todas as tabelas com o filtro especificado
        tabelas = soup.find_all("div", style="overflow-x:auto;margin-bottom:20px;")

        # Itera sobre cada tabela
        for tabela in tabelas:
            linhas = tabela.find_all("tr", class_="text-center")

            # Itera sobre cada linha da tabela
            for linha in linhas:
                colunas = linha.find_all("td")
                if not colunas:
                    continue

                # Coleta os dados do navio
                data_chegada = colunas[4].text.strip()
                volume = colunas[9].decode_contents()
                produto = colunas[8].decode_contents()
                sentido = colunas[7].text.strip()

                existe = NavioBronze.objects.filter(
                    data_chegada=data_chegada,
                    volume=volume,
                    produto=produto,
                    sentido=sentido,
                    porto="Porto de Santos",
                ).exists()

                # Verifica se o valor do objeto já está armazenado, caso contrário, cria um novo objeto
                if not existe:
                    NavioBronze.objects.create(
                        data_chegada=data_chegada,
                        volume=volume,
                        produto=produto,
                        sentido=sentido,
                        porto="Porto de Santos",
                    )
                    
        # Exibe mensagem de sucesso no terminal
        self.stdout.write(self.style.SUCCESS("Importação concluída!"))
