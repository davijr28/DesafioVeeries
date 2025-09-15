#!/bin/bash
# entrypoint.sh

# Garantir que o log exista
touch /var/log/daily_job.log

# Loop infinito para rodar os stages na hora desejada
while true; do
    # Hora atual em Brasília
    HORA=$(date +%H:%M)
    
    # Se for 12:59
    if [ "$HORA" == "12:59" ]; then
        echo "Rodando Bronze e Silver em $(date)" >> /var/log/daily_job.log
        cd /app
        export DJANGO_SETTINGS_MODULE=DesafioVeeries.settings
        /usr/local/bin/python manage.py bronze_stage_paranagua >> /var/log/daily_job.log 2>&1
        /usr/local/bin/python manage.py bronze_stage_santos >> /var/log/daily_job.log 2>&1
        /usr/local/bin/python manage.py silver_stage >> /var/log/daily_job.log 2>&1
        # Espera 61 segundos para não rodar novamente no mesmo minuto
        sleep 61
    else
        # Checa a hora a cada 30 segundos
        sleep 30
    fi
done
