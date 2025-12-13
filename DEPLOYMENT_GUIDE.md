# Burhani Guards API - Deployment Guide

## 📋 Prerequisites
- Python 3.11 or higher
- PostgreSQL database running on AWS server (13.204.161.209)
- SSH access to the server
- Database: `burhani_guards_db` with schema `bg`

## 🔧 Configuration

### 1. Update Environment Variables

Edit the `.env` file and update the password:

```bash
# PostgreSQL Connection Configuration
PG_HOST=127.0.0.1
PG_PORT=5432
PG_DATABASE=burhani_guards_db
PG_USER=abdulkader
PG_PASSWORD=your_actual_password_here  # <-- UPDATE THIS
PG_SCHEMA=bg

# API Configuration
API_BASE_PATH=/BURHANI_GUARDS_API_TEST/api
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Verify Database Function Exists

Connect to PostgreSQL and verify the login function exists:

```bash
psql -U abdulkader -d burhani_guards_db -h 127.0.0.1
```

Then run:
```sql
-- Check if the function exists
SELECT routine_name 
FROM information_schema.routines 
WHERE routine_schema = 'bg' 
AND routine_name = 'com_spr_login_json';

-- Test the function manually
SELECT * FROM bg.com_spr_login_json(
    'CHECK_LOGIN',
    12345678,  -- Replace with actual ITS ID
    'password123',  -- Replace with actual password
    '192.168.1.1'
);
```

## 🚀 Running the API

### Local Development

```bash
# Using uvicorn directly
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Or using the Python script
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Production (using systemd service)

```bash
# Install the service
sudo ./install_service.sh

# Start the service
sudo systemctl start burhani-guards-api

# Enable auto-start on boot
sudo systemctl enable burhani-guards-api

# Check status
sudo systemctl status burhani-guards-api

# View logs
sudo journalctl -u burhani-guards-api -f
```

## 📡 API Endpoints

### Base URL
```
http://13.204.161.209/BURHANI_GUARDS_API_TEST/api
```

### Available Endpoints

#### 1. Health Check
```
GET /BURHANI_GUARDS_API_TEST/api/health
```

Response:
```json
{
  "status": "healthy",
  "api": "Burhani Guards API",
  "version": "1.0.0"
}
```

#### 2. Login Health Check
```
GET /BURHANI_GUARDS_API_TEST/api/Login/health
```

Response:
```json
{
  "status": "healthy",
  "service": "Burhani Guards Login API",
  "database": "PostgreSQL"
}
```

#### 3. Check Login (POST)
```
POST /BURHANI_GUARDS_API_TEST/api/Login/CheckLogin
```

Request Body:
```json
{
  "username": "12345678",
  "password": "your_password"
}
```

Success Response (200):
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "its_id": 12345678,
    "full_name": "John Doe",
    "full_name_arabic": "جون دو",
    "email": "john@example.com",
    "mobile": "+919876543210",
    "whatsapp_mobile": "+919876543210",
    "team_id": 1,
    "team_name": "Security Team A",
    "position_id": 2,
    "position_name": "Guard Captain",
    "jamaat_id": 5,
    "jamaat_name": "Mumbai Central",
    "jamiaat_id": 1,
    "jamiaat_name": "Mumbai",
    "role_id": 3,
    "role_name": "Team Leader",
    "is_admin": false,
    "access_rights": "view_duties,manage_team,view_reports",
    "status": 1
  }
}
```

Failed Response (200):
```json
{
  "success": false,
  "message": "Invalid ITS ID or password",
  "data": null
}
```

### API Documentation

Interactive API documentation is available at:
```
http://13.204.161.209/BURHANI_GUARDS_API_TEST/api/docs
```

ReDoc documentation:
```
http://13.204.161.209/BURHANI_GUARDS_API_TEST/api/redoc
```

## 🧪 Testing

### Using cURL

```bash
# Health check
curl http://13.204.161.209/BURHANI_GUARDS_API_TEST/api/health

# Login test
curl -X POST "http://13.204.161.209/BURHANI_GUARDS_API_TEST/api/Login/CheckLogin" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "12345678",
    "password": "your_password"
  }'
```

### Using Python Test Script

See `test_login_api.py` for automated tests.

## 🔒 Security Notes

1. **Password**: Update the `.env` file with the actual database password
2. **CORS**: In production, update CORS settings in `app/main.py` to allow only specific origins
3. **HTTPS**: Consider setting up SSL/TLS for production
4. **IP Address**: The API logs the client IP address for security auditing

## 🐛 Troubleshooting

### Database Connection Issues

```bash
# Test PostgreSQL connection
psql -U abdulkader -d burhani_guards_db -h 127.0.0.1

# Check if PostgreSQL is running
sudo systemctl status postgresql

# View API logs
sudo journalctl -u burhani-guards-api -f
```

### Common Issues

1. **"Function does not exist"**: Verify the `com_spr_login_json` function is created in the `bg` schema
2. **Connection refused**: Check if PostgreSQL is accepting connections on 127.0.0.1:5432
3. **Authentication failed**: Verify database credentials in `.env`
4. **Module not found**: Run `pip install -r requirements.txt`

## 📁 Project Structure

```
burhani-guards-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── db.py                # Database connection utilities
│   ├── models/
│   │   ├── __init__.py
│   │   └── login.py         # Pydantic models for login
│   └── routers/
│       ├── __init__.py
│       └── Login_controller.py  # Login endpoint handlers
├── .env                     # Environment variables (not in git)
├── .env.example            # Example environment variables
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker configuration
├── deploy.sh               # Deployment script
├── install_service.sh      # systemd service installer
└── README.md              # This file
```

## 🔄 Deployment Workflow

1. Update code on server:
```bash
ssh -i your-key.pem ubuntu@13.204.161.209
cd /path/to/burhani-guards-api
git pull  # If using git
```

2. Restart the service:
```bash
sudo systemctl restart burhani-guards-api
```

3. Verify it's running:
```bash
curl http://localhost:8000/BURHANI_GUARDS_API_TEST/api/health
```

## 📞 Support

For issues or questions, contact the development team.
