FROM python:3.11-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV TZ=America/Sao_Paulo

# Instalar dependências de sistema essenciais
RUN apt-get update && apt-get install -y \
    gcc libxml2-dev libxslt1-dev python3-dev tzdata procps \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o código
COPY . .

# Criar diretório para log
RUN touch /var/log/daily_job.log

# Copiar entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Rodar entrypoint (loop infinito que substitui o cron)
CMD ["/entrypoint.sh"]
