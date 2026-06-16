#!/bin/bash
set -e

echo "=========================================="
echo "Autonomous News Business - Setup Script"
echo "=========================================="

# Step 1: Check dependencies
echo "Step 1: Checking dependencies..."
command -v python3 >/dev/null || { echo "Python 3 required"; exit 1; }
command -v node >/dev/null || { echo "Node.js required"; exit 1; }

# Step 2: Install Python dependencies
echo "Step 2: Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Step 3: Install Node.js dependencies
echo "Step 3: Installing Node.js dependencies..."
cd website
npm install
cd ..

# Step 4: Setup environment
echo "Step 4: Setting up environment..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file. Please fill in your API keys:"
    echo "  - OPENAI_API_KEY"
    echo "  - GROQ_API_KEY"
    echo "  - NEWSAPI_API_KEY"
    echo "  - SUPABASE_URL"
    echo "  - SUPABASE_SERVICE_KEY"
    echo "  - VERCEL_TOKEN"
fi

# Step 5: Create logs directory
echo "Step 5: Creating logs directory..."
mkdir -p logs

# Step 6: Test database connection
echo "Step 6: Testing database connection..."
python3 << 'EOF'
import os
from dotenv import load_dotenv
load_dotenv()

try:
    from db.supabase_client import SupabaseClient
    db = SupabaseClient()
    if db.health_check():
        print("  Database connection: OK")
    else:
        print("  Database connection: FAILED")
except Exception as e:
    print(f"  Database setup required: {e}")
EOF

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env with your API keys"
echo "2. python daemon.py  (start the daemon)"
echo "3. cd website && npm run dev  (start website)"
echo ""
