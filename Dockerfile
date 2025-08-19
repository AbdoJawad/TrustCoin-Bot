# TrustCoin Bot Dockerfile
# Multi-stage build for optimized production image

FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install curl for health checks
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app

# Copy Python dependencies from builder stage
COPY --from=builder /root/.local /home/app/.local

# Copy application code
COPY . .

# Create logs directory
RUN mkdir -p /app/logs && chown -R app:app /app/logs

# Change ownership to app user
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Add local Python packages to PATH
ENV PATH=/home/app/.local/bin:$PATH

# Set Python environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose port (optional, for webhook mode)
EXPOSE 8443

# Health check with better validation
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import sys, os; sys.exit(0 if os.path.exists('/tmp/bot_healthy') else 1)" || exit 1

# Default command (will be overridden by docker-compose)
CMD ["python", "ENGLISH/bot.py"]
    CMD python -c "import requests; requests.get('http://localhost:8443/health')" || exit 1

# Default command (can be overridden in docker-compose)
CMD ["python", "ENGLISH/bot.py"]