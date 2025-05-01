FROM python:3.12-slim

# Install system dependencies for WeasyPrint
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libxml2 \
    libxslt1.1 \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=80
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN mkdir -p /app/staticfiles && chmod -R 777 /app/staticfiles

# Copy app source code
COPY . .

# Create non-root user and switch to it
RUN adduser --disabled-password appuser
USER appuser

# Expose port
EXPOSE 80

# Start Gunicorn
COPY migrate.sh /app/migrate.sh
RUN chmod +x /app/migrate.sh

ENTRYPOINT ["/app/migrate.sh"]

