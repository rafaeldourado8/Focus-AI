FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    postgresql-client \
    redis-tools \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 2>&1 | grep -v "WARNING: Failed to remove"

COPY . .

RUN dos2unix entrypoint.sh && chmod +x entrypoint.sh

EXPOSE 8000

CMD ["./entrypoint.sh"]