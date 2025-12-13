# 🚀 Burhani Guards API - Quick Start Guide

This guide will get your API up and running in 5 minutes!

## ⚡ Quick Setup (5 Steps)

### Step 1: Configure Database Password

Edit the `.env` file and update your database password:

```bash
nano .env
```

Update this line:
```
PG_PASSWORD=your_actual_password_here
```

Save and exit (Ctrl+X, then Y, then Enter)

### Step 2: Verify Database Connection

Test your database connection:

```bash
psql -U abdulkader -d burhani_guards_db -h 127.0.0.1
```

If this works, you're good! Type `\q` to exit.

### Step 3: Verify the Login Function Exists

```bash
psql -U abdulkader -d burhani_guards_db -h 127.0.0.1 -c "SELECT routine_name FROM information_schema.routines WHERE routine_schema = 'bg' AND routine_name = 'com_spr_login_json';"
```

You should see:
```
     routine_name      
-----------------------
 com_spr_login_json
```

If not, you need to deploy the login function first!

### Step 4: Start the API

Simply run:

```bash
./run.sh
```

This script will:
- Create a virtual environment (if needed)
- Install dependencies
- Start the API server

You should see:
```
✅ Setup complete!

🚀 Starting Burhani Guards API...
   URL: http://localhost:8000/BURHANI_GUARDS_API_TEST/api
   Docs: http://localhost:8000/BURHANI_GUARDS_API_TEST/api/docs
```

### Step 5: Test the API

In a new terminal, run:

```bash
# Test health check
curl http://localhost:8000/BURHANI_GUARDS_API_TEST/api/health

# Test login (update with real credentials)
curl -X POST "http://localhost:8000/BURHANI_GUARDS_API_TEST/api/Login/CheckLogin" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "12345678",
    "password": "your_password"
  }'
```

Or use the automated test script:

```bash
# Update test credentials first
nano test_login_api.py  # Update TEST_ITS_ID and TEST_PASSWORD

# Run tests
python3 test_login_api.py
```

## 🌐 Access Points

Once running, you can access:

| Service | URL |
|---------|-----|
| API Base | http://localhost:8000/BURHANI_GUARDS_API_TEST/api |
| Health Check | http://localhost:8000/BURHANI_GUARDS_API_TEST/api/health |
| Login Endpoint | http://localhost:8000/BURHANI_GUARDS_API_TEST/api/Login/CheckLogin |
| Interactive Docs | http://localhost:8000/BURHANI_GUARDS_API_TEST/api/docs |
| ReDoc | http://localhost:8000/BURHANI_GUARDS_API_TEST/api/redoc |

## 📱 Testing from Your Phone/Browser

To test the login endpoint from your phone or browser:

1. Visit: http://localhost:8000/BURHANI_GUARDS_API_TEST/api/docs
2. Find the **POST /Login/CheckLogin** endpoint
3. Click "Try it out"
4. Enter your credentials:
   ```json
   {
     "username": "12345678",
     "password": "your_password"
   }
   ```
5. Click "Execute"

## 🔧 Manual Installation (if run.sh doesn't work)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 📊 Expected Response Format

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
    "access_rights": "view_duties,manage_team",
    "status": 1
  }
}
```

### Failed Login

```json
{
  "success": false,
  "message": "Invalid ITS ID or password",
  "data": null
}
```

## 🐛 Troubleshooting

### Issue: "Connection refused"

**Solution:** Make sure PostgreSQL is running:
```bash
sudo systemctl status postgresql
```

### Issue: "Module not found"

**Solution:** Install requirements:
```bash
pip install -r requirements.txt
```

### Issue: "Function does not exist"

**Solution:** Deploy the login function:
```bash
psql -U abdulkader -d burhani_guards_db -h 127.0.0.1 -f path/to/login_function.sql
```

### Issue: "Authentication failed"

**Solution:** Check your `.env` file has the correct password

## 📞 Need Help?

1. Check the logs in the terminal where you ran `./run.sh`
2. Review the full `DEPLOYMENT_GUIDE.md` for detailed information
3. Test individual components:
   - Database connection
   - Function execution
   - API health endpoint

## ✅ Next Steps

Once your API is running:

1. ✅ Test all endpoints using the test script
2. ✅ Configure your frontend to use this API
3. ✅ Set up production deployment (see DEPLOYMENT_GUIDE.md)
4. ✅ Configure CORS for your frontend domain
5. ✅ Set up SSL/TLS for production use

---

**That's it! You're ready to go! 🎉**

For detailed information, see `DEPLOYMENT_GUIDE.md`
