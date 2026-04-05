FROM python:3.12-slim

# Security: run as non-root
RUN adduser --disabled-password --gecos "" scraper
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy scripts
COPY scraper.py .
COPY agents.py .
COPY backfill_wayback.py .
COPY config.json .

# Run as non-root
USER scraper

# Cloud Run Jobs call the entrypoint and expect it to exit 0 on success
ENTRYPOINT ["python", "-u", "scraper.py"]
