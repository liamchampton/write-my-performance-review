# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Copy requirements first for better caching
COPY requirements.txt .

# Upgrade pip first
RUN pip install --upgrade pip

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt || \
    (echo "Failed to install requirements. Trying without eval_type_backport..." && \
     pip install --no-cache-dir Flask==3.0.3 flask-cors==4.0.0 azure-ai-inference>=1.0.0 azure-core>=1.30.0 "urllib3<2")

# Copy application code
COPY . .

# Create a volume mount point for persistent data
VOLUME ["/app/data"]

# Expose the application port
EXPOSE 8080

# Run the application
CMD ["python", "app.py"]
