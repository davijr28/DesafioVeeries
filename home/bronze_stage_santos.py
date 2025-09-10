import requests
from bs4 import BeautifulSoup

page_santos = requests.get(
    "https://www.portodesantos.com.br/informacoes-operacionais/operacoes-portuarias/navegacao-e-movimento-de-navios/navios-esperados-carga",
    verify=False,
)
dados_santos = BeautifulSoup(page_santos.text, "html.parser")

dadoraw = dados_santos.find_all("div", style="overflow-x:auto;margin-bottom:20px;")
for table in dadoraw:
    dados = table.find_all("tr", class_="text-center")
    print(dados)
