# Usa immagine ufficiale Python 3.11 slim
FROM python:3.11-slim

# Setta la working directory
WORKDIR /app

# Copia i file requirements.txt e installa dipendenze
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia tutto il resto del codice
COPY . .

# Comando per avviare il bot (modifica se serve)
CMD ["python", "rss_gpt_bot.py"]
