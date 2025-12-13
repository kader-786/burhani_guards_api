#!/bin/bash
# Burhani Guards API Startup Script

echo "=========================================="
echo "  Burhani Guards API Server"
echo "=========================================="
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "   Please copy .env.example to .env and configure it"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update requirements
echo "📥 Installing requirements..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Starting Burhani Guards API..."
echo "   URL: http://localhost:8000/BURHANI_GUARDS_API_TEST/api"
echo "   Docs: http://localhost:8000/BURHANI_GUARDS_API_TEST/api/docs"
echo ""
echo "   Press Ctrl+C to stop the server"
echo ""

# Start the API
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
