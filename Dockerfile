FROM python:3.12-slim

# Instala o Chromium e o Driver. O apt resolve as dependências visuais sozinho.
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV CHROME_BIN=/usr/bin/chromium

CMD ["python", "-u", "main.py"]