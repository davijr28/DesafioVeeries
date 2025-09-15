#!/bin/bash
# entrypoint.sh

# Garantir que o log exista
touch /var/log/daily_job.log

# Função para rodar Bronze e Silver
run_stages() {
    echo "Rodando Bronze e Silver em $(date)" >> /var/log/daily_job.log
    cd /app
    export DJANGO_SETTINGS_MODULE=DesafioVeeries.settings
    /usr/local/bin/python manage.py bronze_stage_paranagua >> /var/log/daily_job.log 2>&1
    /usr/local/bin/python manage.py bronze_stage_santos >> /var/log/daily_job.log 2>&1
    /usr/local/bin/python manage.py silver_stage >> /var/log/daily_job.log 2>&1
}

# Rodar imediatamente na primeira vez
run_stages

# Loop infinito para rodar diariamente no horário definido
while true; do
    HORA=$(date +%H:%M)  # horário do container 
    
    if [ "$HORA" == "01:26" ]; then
        run_stages
        # Espera 61 segundos para não rodar duas vezes no mesmo minuto
        sleep 61
    else
        sleep 30
    fi
done
