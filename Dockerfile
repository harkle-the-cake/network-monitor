FROM python:3.11-slim

# Installiere benötigte Systemtools inkl. ping & nmap
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        nmap \
        iputils-ping \
        net-tools \
        gcc \
        libffi-dev \
        libssl-dev \
        build-essential \
        python3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Setze Arbeitsverzeichnis
WORKDIR /app

# Abhängigkeiten
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App & statische Dateien
COPY app.py ./
COPY static ./static

# Flask App starten
CMD ["python", "app.py"]
