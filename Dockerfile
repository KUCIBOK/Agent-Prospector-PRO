FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Playwright system dependencies
RUN apt-get update && apt-get install -y \
    libnss3 libxss1 libasound2 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2 libgbm1 libnss3 libpangocairo-1.0-0 \
    libu2f-udev libvulkan1 libxcb-dri3-0 libxdamage1 libxfixes3 \
    libxkbcommon0 libxrandr2 fonts-liberation libu2f-udev libvulkan1 xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip setuptools wheel

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install

# Copy application code
COPY app ./app
COPY scripts ./scripts

# Create logs directory
RUN mkdir -p logs

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default command (can be overridden)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
