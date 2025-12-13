FROM python:3.11-slim

# Install PostgreSQL client libraries
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set workdir and copy files
WORKDIR /app
COPY requirements.txt .

# Install Python packages
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Docker commands:
# docker stop burhani-guards-api
# docker rm burhani-guards-api
# docker build -t burhani-guards-api .
# docker run -d -p 8000:8000 --name burhani-guards-api burhani-guards-api
