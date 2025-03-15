#!/bin/bash

# Script to restart the investment platform with full simulation mode

echo "=========================================================="
echo "RESTARTING INVESTMENT PLATFORM WITH FULL SIMULATION"
echo "=========================================================="

# Navigate to the project directory
cd "$(dirname "$0")"

# Kill any running uvicorn processes
echo "Stopping any running servers..."
pkill -f uvicorn 2>/dev/null || true

# Free up port 8000
if command -v lsof >/dev/null 2>&1; then
    lsof -i :8000 -t | xargs kill -9 2>/dev/null || true
fi

# Wait for port to be completely free
sleep 2

echo "Starting server with full simulation mode..."
echo "=========================================================="

# Start the server
python run.py

echo "Server started with full simulation mode!" 