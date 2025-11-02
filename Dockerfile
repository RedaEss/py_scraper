# Dockerfile - VERSION OPTIMISÉE
FROM python:3.9-slim

WORKDIR /app

# Installation des dépendances système pour lxml
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY scraper.py .
COPY run_scraper.py .

CMD ["python", "run_scraper.py"]