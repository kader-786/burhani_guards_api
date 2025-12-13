# 🎯 Burhani Guards API - Complete Setup Instructions

This document provides step-by-step instructions to set up and deploy the Burhani Guards FastAPI application.

## 📦 What's Included

Your API project includes:

```
burhani-guards-api/
├── app/                          # Application code
│   ├── main.py                  # FastAPI app entry point
│   ├── config.py                # Configuration management
│   ├── db.py                    # Database connection & utilities
│   ├── models/
│   │   └── login.py            # Pydantic models
│   └── routers/
│       └── Login_controller.py # Login endpoint
├── .env                         # Environment variables (CONFIGURE THIS!)
├── .env.example                 # Template for .env
├── requirements.txt             # Python dependencies
├── run.sh                       # Quick start script
├── preflight_check.py          # Setup verification script
├── test_login_api.py           # API test suite
├── QUICKSTART.md               # 5-minute setup guide
├── DEPLOYMENT_GUIDE.md         # Detailed deployment docs
└── README.md                   # Project overview
```

## 🚀 Option 1: Quick Start (5 Minutes)

### Step 1: Upload Files to Server

SSH into your server and create project directory:

```bash
ssh -i your-key.pem ubuntu@13.204.161.209
mkdir -p ~/burhani-guards-api
cd ~/burhani-guards-api
```

Upload all files to this directory using SCP or your preferred method.

### Step 2: Configure Database Password

```bash
cd ~/burhani-guards-api
nano .env
```

Update this line with your actual PostgreSQL password:
```
PG_PASSWORD=your_actual_password_here
```

Save (Ctrl+X, Y, Enter)

### Step 3: Run Pre-flight Check

```bash
python3 preflight_check.py
```

This will verify:
- ✅ Python version
- ✅ Environment configuration
- ✅ Required packages
- ✅ Database connectivity
- ✅ Login function exists

### Step 4: Start the API

```bash
./run.sh
```

The API will start on port 8000!

### Step 5: Test It!

In another terminal:

```bash
# Test health
curl http://localhost:8000/BURHANI_GUARDS_API_TEST/api/health

# Test login (use real credentials)
curl -X POST "http://localhost:8000/BURHANI_GUARDS_API_TEST/api/Login/CheckLogin" \
  -H "Content-Type: application/json" \
  -d '{"username": "12345678", "password": "your_password"}'
```

**Done! Your API is running! 🎉**

---

## 🔧 Option 2: Manual Installation

### Prerequisites

1. **Python 3.8 or higher**
   ```bash
   python3 --version
   ```

2. **PostgreSQL 12 or higher**
   ```bash
   psql --version
   ```

3. **pip package manager**
   ```bash
   pip3 --version
   ```

### Installation Steps

#### 1. Create Project Directory

```bash
mkdir -p ~/burhani-guards-api
cd ~/burhani-guards-api
```

#### 2. Upload All Files

Transfer all project files to this directory.

#### 3. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# OR
venv\Scripts\activate     # On Windows
```

#### 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 5. Configure Environment

```bash
cp .env.example .env
nano .env
```

Update these values:
```bash
PG_HOST=127.0.0.1
PG_PORT=5432
PG_DATABASE=burhani_guards_db
PG_USER=abdulkader
PG_PASSWORD=YOUR_ACTUAL_PASSWORD_HERE  # <-- CHANGE THIS
PG_SCHEMA=bg

API_BASE_PATH=/BURHANI_GUARDS_API_TEST/api
```

#### 6. Verify Database Function Exists

```bash
psql -U abdulkader -d burhani_guards_db -h 127.0.0.1
```

In psql:
```sql
-- Check if function exists
SELECT routine_name 
FROM information_schema.routines 
WHERE routine_schema = 'bg' 
AND routine_name = 'com_spr_login_json';
```

You should see `com_spr_login_json` listed. If not, deploy it first!

Exit psql:
```sql
\q
```

#### 7. Run Pre-flight Check

```bash
python3 preflight_check.py
```

All checks should pass!

#### 8. Start the Server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Database connection pool initialized
INFO:     Application startup complete.
```

---

## 🧪 Testing Your Installation

### 1. Health Check Test

```bash
curl http://localhost:8000/BURHANI_GUARDS_API_TEST/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "api": "Burhani Guards API",
  "version": "1.0.0"
}
```

### 2. Login Health Check

```bash
curl http://localhost:8000/BURHANI_GUARDS_API_TEST/api/Login/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Burhani Guards Login API",
  "database": "PostgreSQL"
}
```

### 3. Login Test

```bash
curl -X POST "http://localhost:8000/BURHANI_GUARDS_API_TEST/api/Login/CheckLogin" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "12345678",
    "password": "your_password"
  }'
```

Success response:
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "its_id": 12345678,
    "full_name": "John Doe",
    "email": "john@example.com",
    "team_name": "Security Team A",
    ...
  }
}
```

### 4. Run Full Test Suite

```bash
# First, update test credentials
nano test_login_api.py
# Change TEST_ITS_ID and TEST_PASSWORD

# Run tests
python3 test_login_api.py
```

---

## 🌐 Accessing from Browser

### Interactive API Documentation

Visit these URLs in your browser:

1. **Swagger UI (Interactive)**
   ```
   http://localhost:8000/BURHANI_GUARDS_API_TEST/api/docs
   ```
   - Try out API endpoints directly
   - See request/response formats
   - Test authentication

2. **ReDoc (Alternative)**
   ```
   http://localhost:8000/BURHANI_GUARDS_API_TEST/api/redoc
   ```
   - Clean, organized documentation
   - Better for reading

### Testing Login in Browser

1. Go to: `http://localhost:8000/BURHANI_GUARDS_API_TEST/api/docs`
2. Find **POST /Login/CheckLogin**
3. Click "Try it out"
4. Enter:
   ```json
   {
     "username": "12345678",
     "password": "your_password"
   }
   ```
5. Click "Execute"
6. See the response!

---

## 🚢 Production Deployment

### Using systemd Service (Recommended)

1. **Install the service**
   ```bash
   sudo ./install_service.sh
   ```

2. **Start the service**
   ```bash
   sudo systemctl start burhani-guards-api
   ```

3. **Enable auto-start on boot**
   ```bash
   sudo systemctl enable burhani-guards-api
   ```

4. **Check status**
   ```bash
   sudo systemctl status burhani-guards-api
   ```

5. **View logs**
   ```bash
   sudo journalctl -u burhani-guards-api -f
   ```

### Configure Nginx (Optional)

If you want to serve on port 80 with a domain name:

1. Install Nginx:
   ```bash
   sudo apt install nginx
   ```

2. Create config:
   ```bash
   sudo nano /etc/nginx/sites-available/burhani-guards-api
   ```

3. Add this configuration:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location /BURHANI_GUARDS_API_TEST/api {
           proxy_pass http://localhost:8000/BURHANI_GUARDS_API_TEST/api;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       }
   }
   ```

4. Enable and restart:
   ```bash
   sudo ln -s /etc/nginx/sites-available/burhani-guards-api /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

---

## 🔒 Security Checklist

- [ ] Updated `.env` with strong database password
- [ ] Configured CORS to allow only trusted domains
- [ ] Set up SSL/TLS certificate (use Let's Encrypt)
- [ ] Enabled firewall (ufw or iptables)
- [ ] Regular database backups configured
- [ ] Monitoring and alerting set up
- [ ] Log rotation configured

---

## 🐛 Troubleshooting Guide

### Issue: "Connection refused"

**Cause:** PostgreSQL not running or not accepting connections

**Solution:**
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Start if stopped
sudo systemctl start postgresql

# Test connection
psql -U abdulkader -d burhani_guards_db -h 127.0.0.1
```

### Issue: "Function does not exist"

**Cause:** `com_spr_login_json` function not deployed

**Solution:**
```bash
# Deploy the function
psql -U abdulkader -d burhani_guards_db -h 127.0.0.1 -f path/to/login_function.sql
```

### Issue: "Module not found: fastapi"

**Cause:** Dependencies not installed

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "Authentication failed for user"

**Cause:** Wrong password in `.env`

**Solution:**
```bash
nano .env
# Update PG_PASSWORD with correct password
```

### Issue: Port 8000 already in use

**Cause:** Another process using port 8000

**Solution:**
```bash
# Find the process
sudo lsof -i :8000

# Kill it (replace PID)
kill -9 PID

# Or use a different port
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

---

## 📊 Understanding the Response Format

### Successful Login

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
    "gender": "M",
    "age": 30,
    "address": "123 Main St",
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

### Failed Login - Wrong Password

```json
{
  "success": false,
  "message": "Invalid password",
  "data": null
}
```

### Failed Login - Invalid ITS ID

```json
{
  "success": false,
  "message": "Invalid ITS ID or account is not active",
  "data": null
}
```

---

## 📚 Additional Resources

- **QUICKSTART.md** - 5-minute setup guide
- **DEPLOYMENT_GUIDE.md** - Comprehensive deployment documentation
- **API_TESTING.md** - Testing strategies and tools
- **README.md** - Project overview

---

## 🎯 Next Steps

After successful deployment:

1. ✅ **Integrate with Frontend**
   - Update frontend API base URL to point to your server
   - Implement login flow using the `/Login/CheckLogin` endpoint

2. ✅ **Add More Endpoints**
   - Duty management
   - Miqaat scheduling
   - Attendance tracking
   - Team management

3. ✅ **Set Up Monitoring**
   - Application logs
   - Database performance
   - API response times
   - Error tracking

4. ✅ **Configure Backups**
   - Database backups
   - Application logs
   - Configuration files

5. ✅ **Security Hardening**
   - SSL/TLS certificates
   - Firewall rules
   - Rate limiting
   - API authentication tokens

---

## 📞 Need Help?

1. **Run diagnostics:**
   ```bash
   python3 preflight_check.py
   ```

2. **Check logs:**
   ```bash
   # Development mode
   # Logs appear in terminal

   # Production mode (systemd)
   sudo journalctl -u burhani-guards-api -f
   ```

3. **Test individual components:**
   - Database connection: `psql -U abdulkader -d burhani_guards_db -h 127.0.0.1`
   - Python environment: `python3 --version`
   - Packages: `pip list`

---

**Congratulations! Your Burhani Guards API is ready! 🎉**

Access your API documentation at:
**http://13.204.161.209/BURHANI_GUARDS_API_TEST/api/docs**
