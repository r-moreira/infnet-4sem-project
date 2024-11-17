FROM python:3.11.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libfreetype6-dev \
    libpng-dev \
    libjpeg-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

#COPY config.yml .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "PYTHONPATH=./src uvicorn src.app:app --host 0.0.0.0 --port 8000"]