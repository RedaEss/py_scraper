# Dockerfile - AVEC PANDAS COMPATIBLE
FROM python:3.9-slim

# Installation des dépendances système pour pandas et lxml
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY scraper.py .
COPY run_scraper.py .

CMD ["python", "run_scraper.py"]