# Dockerfile
FROM python:3.9-slim

# Installation des dépendances système minimales
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copie et installation des packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie des scripts
COPY scraper.py .
COPY run_scraper.py .

# Commande par défaut
CMD ["python", "run_scraper.py"]