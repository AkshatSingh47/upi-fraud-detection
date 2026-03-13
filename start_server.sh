#!/bin/bash

echo "========================================"
echo "UPI Fraud Detection - Starting Servers"
echo "========================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 is not installed"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "[ERROR] Node.js is not installed"
    exit 1
fi

echo ""
echo "[1/6] Setting up Python virtual environment..."
if [ ! -d "backend/venv" ]; then
    echo "Creating virtual environment..."
    cd backend
    python3 -m venv venv
    cd ..
fi

echo ""
echo "[2/6] Installing backend dependencies..."
cd backend
source venv/bin/activate
pip install -r requirements.txt
cd ..

echo ""
echo "[3/6] Training ML model..."
cd ml
source ../backend/venv/bin/activate
python3 retrain_model.py
cd ..

echo ""
echo "[4/6] Installing frontend dependencies..."
cd frontend
if [ ! -d "node_modules" ]; then
    npm install
fi
cd ..

echo ""
echo "[5/6] Starting Backend Server (Port 8000)..."
cd backend
source venv/bin/activate
python3 run.py &
BACKEND_PID=$!
cd ..

sleep 3

echo ""
echo "[6/6] Starting Frontend Server (Port 3000)..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "========================================"
echo "✓ Servers are running!"
echo "========================================"
echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID

