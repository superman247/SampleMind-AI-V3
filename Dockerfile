# syntax=docker/dockerfile:1.4

# Build stage
FROM python:3.11-slim-bullseye AS builder

# Upgrade pip and system packages to reduce vulnerabilities
RUN apt-get update && apt-get upgrade -y && pip install --upgrade pip && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.11-slim-bullseye

# Set working directory
WORKDIR /app

# Copy from builder stage
COPY --from=builder /app /app

# Copy the rest of the application code
COPY . .

# Copy llm_client.py specifically
COPY core/llm_client.py /app/

# Create a non-root user and switch to it
RUN useradd --create-home appuser
USER appuser

# Expose the port your app runs on (adjust if needed)
EXPOSE 8000

# Set environment variables (optional, adjust as needed)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/usr/local/bin:$PATH"

# HEALTHCHECK instruction to monitor the application's health
HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD curl -f http://localhost:8000/health || exit 1

# Run the application (adjust command as needed)
CMD ["uvicorn", "core.llm_client:app", "--host", "0.0.0.0", "--port", "8000"]