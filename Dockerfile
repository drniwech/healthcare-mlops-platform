# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install system + Python dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

# Copy entire project
COPY . .

# Environment variable
ENV PYTHONUNBUFFERED=1

# Run training
CMD ["python", "training/train.py"]
