# Desafio Veeries: Lineup de Navios - ETL Diário de Volumes Portuários

## Descrição do Projeto
Este projeto coleta e atualiza diariamente informações sobre o lineup de navios esperados nos portos de **Paranaguá** e **Santos**. O objetivo é monitorar os **volumes transportados diariamente**, classificados por **produto**, **data**, **volume**, **sentido** (exportação/importação) e **porto**, mantendo o **histórico completo** dos dados.

O fluxo de dados segue a **arquitetura medallion**, garantindo dados brutos, processados e enriquecidos para análise:

- **Bronze**: Dados brutos coletados diretamente das fontes.
- **Silver (Prata)**: Dados processados e padronizados.
- **Gold (Ouro)**: Dados enriquecidos, agregados e prontos para visualização.

---

## Fontes de Dados
- [Porto de Paranaguá](https://www.appaweb.appa.pr.gov.br/appaweb/pesquisa.aspx?WCI=relLineUpRetroativo)  
- [Porto de Santos](https://www.portodesantos.com.br/informacoes-operacionais/operacoesportuarias/navegacao-e-movimento-de-navios/navios-esperados-carga/)  

---

## Arquitetura Medallion

### Bronze
- Scripts:
  - `bronze_stage_paranagua.py`
  - `bronze_stage_santos.py`
- Função: Coleta os dados brutos dos portos e os armazena em banco de dados SQLite.

### Silver (Prata)
- Script:
  - `silver_stage.py`
- Função: Limpa e padroniza os dados brutos, garantindo consistência e integridade, e os armazena em um novo banco de dados SQLite.

### Gold (Ouro)
- Função:
  - `gold_volume_diario` em `views.py`
- Função: Enriquecimento e agregação diária dos volumes, prontos para consumo e visualização.

---


## Tecnologias Utilizadas
- Python 3.x  
- Django 5.x  
- requests  
- BeautifulSoup4  
- lxml  
- SQLite  
- Docker + Docker Compose  
- Execução automatizada via `entrypoint.sh`

---

## Execução

### Com Docker
1. Build do container:
```bash
docker compose build
```
Rodar o projeto com atualização automática diária:

```bash
docker compose up
```
Ao iniciar, o container executa automaticamente os stages Bronze, Silver e Gold, mantendo o histórico dos dados atualizado diariamente.

## Validação e Qualidade dos Dados:
Os dados já são validados nos scripts antes de serem inseridos no banco.

Dados incompletos ou ausentes são registrados como None.

Histórico é preservado em todas as camadas da arquitetura.


## Dicionários de Dados:
Os dados coletados já são padronizados e explicados nas tabelas. A seguir, um resumo das principais colunas e seus valores possíveis:

**- Data:** data de chegada do navio no porto.

**- Produto:** nome do produto transportado pelo navio (ex.: Sal, Milho, Fertilizante, etc.).

**- Sentido:** indica se a operação é de Importação, Exportação ou Importação/Exportação.

**- Volume:** quantidade do produto transportada pelo navio no dia, em unidade padronizada(toneladas).

**- Volume Diário Transportado:** o total de carga transportada no dia.

**- Porto:** Porto de movimentação, atualmente limitado a Paranaguá ou Santos.


## Ideias Futuras:
Melhorar alertas e notificações para inconsistências ou falhas na coleta de dados.

Expandir para outros portos ou fontes de dados.

Adicionar novas métricas ou visualizações nas tabelas existente.

Expandir relatórios diários.

## Autor:
## Davi Jordani Ramos
