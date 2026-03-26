# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY training/ ./training/

# Set environment variables (optional)
ENV PYTHONUNBUFFERED=1

# Run training script
CMD ["python", "training/train.py"]
