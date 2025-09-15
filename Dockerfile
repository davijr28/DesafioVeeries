FROM python:3.11-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV TZ=America/Sao_Paulo

# Instalar dependências de sistema, cron, utilitários e timezone
RUN apt-get update && apt-get install -y \
    gcc libxml2-dev libxslt1-dev python3-dev cron tzdata procps \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o código
COPY . .

# Copiar arquivo de cron para dentro do container
COPY cron/daily_job.cron /etc/cron.d/daily_job
RUN chmod 0644 /etc/cron.d/daily_job

# Criar diretório para log
RUN touch /var/log/daily_job.log

# Rodar cron em foreground com logs
CMD ["cron", "-f", "-L", "15"]
