FROM python:3.11-slim

# 1. Install curl and gnupg for Microsoft ODBC repo
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# 2. Add MS SQL ODBC driver repo and install it
RUN curl -sSL https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl -sSL https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && rm -rf /var/lib/apt/lists/*

# 3. Install dependencies for pyodbc
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    unixodbc \
    unixodbc-dev \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set workdir and copy files
WORKDIR /app
COPY . .

# Install Python packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose FastAPI port
EXPOSE 8000

# Run app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# docker stop hgvdg-python-api
# docker rm hgvdg-python-api

# docker build -t hgvdg-python-api .     
# docker run -d -p 8000:8000 --name hgvdg-python-api hgvdg-python-api