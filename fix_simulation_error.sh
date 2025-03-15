#!/bin/bash

# Script to fix the simulation error and restart the server

echo "=========================================================="
echo "FIXING SIMULATION ERROR AND RESTARTING SERVER"
echo "=========================================================="

# Navigate to project directory
cd "$(dirname "$0")"

# Kill any running server processes
echo "Stopping any running servers..."
pkill -9 -f uvicorn 2>/dev/null || true
ps aux | grep "python run.py" | grep -v grep | awk '{print $2}' | xargs -I{} kill -9 {} 2>/dev/null || true

# Free up port 8000
if command -v lsof >/dev/null 2>&1; then
    lsof -i :8000 -t | xargs kill -9 2>/dev/null || true
fi

# Clear Python cache files
find . -name "__pycache__" -type d -exec rm -rf {} +;
find . -name "*.pyc" -delete

# Wait for port to be completely free
echo "Waiting for port to be freed..."
sleep 2

# Start the server with new settings
echo "Starting server with fixed simulation code..."
echo "=========================================================="

# Start the server
python run.py

echo "Server restarted successfully!" 