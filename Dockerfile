FROM python:slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    docker.io \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency files
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set up volume mount point for source code
VOLUME ["/app/src"]

# Expose Flask port
EXPOSE 5000

# Set environment variables for development
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
ENV PYTHONUNBUFFERED=1

# Development server with auto-reload
CMD ["python", "src/app.py"]