FROM python:3.12-slim

# Security: run as non-root
RUN adduser --disabled-password --gecos "" scraper
WORKDIR /app

# Install system deps for Playwright Chromium
RUN apt-get update && apt-get install -y --no-install-recommends \
    libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
    libdrm2 libdbus-1-3 libxkbcommon0 libatspi2.0-0 \
    libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 \
    libpango-1.0-0 libcairo2 libasound2 libx11-xcb1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright + Chromium browser
RUN playwright install chromium

# Copy scripts
COPY scraper.py .
COPY agents.py .
COPY backfill_wayback.py .
COPY config.json .

# Create output dir for screenshots (owned by scraper user)
RUN mkdir -p /app/output/screenshots && chown -R scraper:scraper /app/output

# Run as non-root
USER scraper

# Cloud Run Jobs call the entrypoint and expect it to exit 0 on success
ENTRYPOINT ["python", "-u", "scraper.py"]
