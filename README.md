# Burhani Guards API

FastAPI-based REST API for the Burhani Guards Management System, connected to PostgreSQL database.

## Features

- User authentication and login
- PostgreSQL database integration
- Connection pooling for better performance
- CORS support for frontend integration
- Comprehensive logging
- Docker support for easy deployment

## Prerequisites

- Python 3.11+
- PostgreSQL 12+
- pip (Python package manager)

## Project Structure

```
burhani_guards_api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration management
│   ├── db.py                # Database connection management
│   ├── models/
│   │   └── login.py         # Pydantic models
│   └── routers/
│       └── Login_controller.py  # Login endpoints
├── .env                     # Environment variables (create from .env.example)
├── .env.example             # Environment variables template
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── run.py                  # Development server runner
└── README.md               # This file
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd burhani_guards_api
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv

# On Linux/Mac
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` and update the following:

```env
PG_HOST=127.0.0.1
PG_PORT=5432
PG_DATABASE=burhani_guards_db
PG_USER=abdulkader
PG_PASSWORD=your_actual_password
PG_SCHEMA=bg
API_BASE_PATH=/BURHANI_GUARDS_API_TEST/api
```

### 5. Run the Application

#### Local Development

```bash
python run.py
```

Or using uvicorn directly:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
- API Base: `http://localhost:8000/BURHANI_GUARDS_API_TEST/api`
- API Docs: `http://localhost:8000/BURHANI_GUARDS_API_TEST/api/docs`
- Health Check: `http://localhost:8000/BURHANI_GUARDS_API_TEST/api/health`

## API Endpoints

### Login

#### POST `/BURHANI_GUARDS_API_TEST/api/Login/CheckLogin`

Authenticate a user and return user details.

**Request Body:**
```json
{
  "username": "12345678",
  "password": "your_password"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "its_id": 12345678,
    "full_name": "John Doe",
    "role_id": 1,
    "team_id": 1,
    "email": "john@example.com",
    ...
  }
}
```

**Response (Failure):**
```json
{
  "success": false,
  "message": "Invalid username or password",
  "data": null
}
```

### Health Check

#### GET `/BURHANI_GUARDS_API_TEST/api/Login/health`

Check if the Login service is running.

**Response:**
```json
{
  "status": "healthy",
  "service": "Burhani Guards Login API",
  "database": "PostgreSQL"
}
```

## Docker Deployment

### Build Docker Image

```bash
docker build -t burhani-guards-api .
```

### Run Docker Container

```bash
docker run -d \
  -p 8000:8000 \
  --name burhani-guards-api \
  --env-file .env \
  burhani-guards-api
```

### Stop and Remove Container

```bash
docker stop burhani-guards-api
docker rm burhani-guards-api
```

## Deployment on AWS Server

### 1. Upload Files to Server

```bash
scp -i "BG_Server.pem" -r ./* ubuntu@13.204.161.209:/home/ubuntu/burhani_guards_api/
```

### 2. SSH into Server

```bash
ssh -i "BG_Server.pem" ubuntu@13.204.161.209
```

### 3. Navigate to Project Directory

```bash
cd /home/ubuntu/burhani_guards_api
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment

Edit the `.env` file with the correct database credentials:

```bash
nano .env
```

### 6. Run with Systemd (Production)

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/burhani-guards-api.service
```

Add the following content:

```ini
[Unit]
Description=Burhani Guards FastAPI Application
After=network.target postgresql.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/burhani_guards_api
Environment="PATH=/home/ubuntu/burhani_guards_api/venv/bin"
ExecStart=/home/ubuntu/burhani_guards_api/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable burhani-guards-api
sudo systemctl start burhani-guards-api
sudo systemctl status burhani-guards-api
```

### 7. Configure Nginx (if needed)

If you need to proxy the API through Nginx:

```bash
sudo nano /etc/nginx/sites-available/burhani-guards-api
```

Add:

```nginx
server {
    listen 80;
    server_name 13.204.161.209;

    location /BURHANI_GUARDS_API_TEST/ {
        proxy_pass http://127.0.0.1:8000/BURHANI_GUARDS_API_TEST/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable and restart Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/burhani-guards-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Testing the API

### Using curl

```bash
# Test login
curl -X POST "http://13.204.161.209/BURHANI_GUARDS_API_TEST/api/Login/CheckLogin" \
  -H "Content-Type: application/json" \
  -d '{"username": "12345678", "password": "your_password"}'

# Test health check
curl "http://13.204.161.209/BURHANI_GUARDS_API_TEST/api/Login/health"
```

### Using Python

```python
import requests

# Test login
response = requests.post(
    "http://13.204.161.209/BURHANI_GUARDS_API_TEST/api/Login/CheckLogin",
    json={"username": "12345678", "password": "your_password"}
)
print(response.json())
```

### Using the Interactive API Documentation

Navigate to: `http://13.204.161.209/BURHANI_GUARDS_API_TEST/api/docs`

## Logging

The application logs are configured to output to the console. In production, you can redirect these to a file:

```bash
# View systemd service logs
sudo journalctl -u burhani-guards-api -f
```

## Troubleshooting

### Database Connection Issues

1. Verify PostgreSQL is running:
   ```bash
   sudo systemctl status postgresql
   ```

2. Check if the database exists:
   ```bash
   psql -U abdulkader -d burhani_guards_db -h 127.0.0.1 -c "SELECT version();"
   ```

3. Verify the function exists:
   ```bash
   psql -U abdulkader -d burhani_guards_db -h 127.0.0.1 -c "SELECT routine_name FROM information_schema.routines WHERE routine_schema = 'bg' AND routine_name = 'com_spr_login_json';"
   ```

### Port Already in Use

If port 8000 is already in use:

```bash
# Find the process
sudo lsof -i :8000

# Kill the process
sudo kill -9 <PID>
```

### Permission Issues

If you encounter permission issues:

```bash
# Change ownership
sudo chown -R ubuntu:ubuntu /home/ubuntu/burhani_guards_api

# Make run.py executable
chmod +x run.py
```

## Development

### Adding New Endpoints

1. Create a new model in `app/models/`
2. Create a new controller in `app/routers/`
3. Register the router in `app/main.py`

### Database Functions

All database interactions should use the functions in `app/db.py`:

- `get_db_connection()` - Get a connection from the pool
- `call_function()` - Call a PostgreSQL function
- `execute_query()` - Execute a raw SQL query

## Security Notes

- Never commit the `.env` file with real credentials
- Use strong passwords for database users
- In production, restrict CORS origins
- Consider implementing rate limiting
- Use HTTPS in production
- Keep dependencies updated

## License

[Your License Here]

## Contact

For issues and questions, contact: [Your Contact Info]
