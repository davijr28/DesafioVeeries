import requests
from bs4 import BeautifulSoup

page_paranagua = requests.get(
    "https://www.appaweb.appa.pr.gov.br/appaweb/pesquisa.aspx?WCI=relLineUpRetroativo"
)
dados_paranagua = BeautifulSoup(page_paranagua.text, "html.parser")

tables = dados_paranagua.find_all(
    "table", class_="table table-bordered table-striped table-hover"
)
for table in tables:
    rows = table.find_all("tbody")
    for row in rows:
        dado = row.find_all("tr")
        print(dado)
