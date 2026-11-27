#!/usr/bin/env bash
# Quickstart script to run POWERGRID Material Forecasting Backend & Frontend

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/SIH_Powergrid/backend"
FRONTEND_DIR="$SCRIPT_DIR/SIH_Powergrid/frontend"

echo "=========================================================="
echo "⚡ Starting POWERGRID Material Demand Forecasting System"
echo "=========================================================="

# Check Python dependencies
echo "📦 Checking Python requirements..."
pip install -r "$BACKEND_DIR/requirements.txt" --quiet

# Seed Database
echo "🌱 Initializing database & seed data..."
cd "$BACKEND_DIR"
python3 seed_db.py

# Start Backend Server
echo "🚀 Starting FastAPI Backend at http://127.0.0.1:8000..."
python3 -m uvicorn app:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!

# Trap Ctrl+C to kill background processes
trap "echo 'Stopping servers...'; kill $BACKEND_PID 2>/dev/null || true; exit" SIGINT SIGTERM EXIT

# Start Frontend Server
echo "🌐 Starting Frontend Web Server at http://127.0.0.1:3000..."
cd "$FRONTEND_DIR"
python3 -m http.server 3000 &
FRONTEND_PID=$!

echo ""
echo "=========================================================="
echo "✅ Systems are running!"
echo "   - Frontend UI: http://127.0.0.1:3000/index.html"
echo "   - Backend API: http://127.0.0.1:8000"
echo "   - Swagger API Docs: http://127.0.0.1:8000/docs"
echo "=========================================================="
echo "Press Ctrl+C to stop both servers."

wait $BACKEND_PID
