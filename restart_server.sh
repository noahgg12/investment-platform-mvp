#!/bin/bash

# Navigate to the project directory
cd "$(dirname "$0")"

echo "=========================================================================="
echo "RESTARTING AI INVESTMENT PLATFORM WITH ENHANCED SIMULATIONS"
echo "=========================================================================="

# Kill any existing uvicorn processes
echo "Stopping any running servers..."
pkill -f uvicorn

# Make sure all Python processes related to the app are terminated
echo "Ensuring no lingering processes..."
ps aux | grep "python run.py" | grep -v grep | awk '{print $2}' | xargs -I {} kill -9 {} 2>/dev/null

# Wait a moment for processes to terminate
sleep 2

# Check if port 8000 is in use
if lsof -i :8000 > /dev/null 2>&1; then
    echo "Port 8000 is still in use. Forcefully terminating processes..."
    lsof -i :8000 -t | xargs kill -9 2>/dev/null
    sleep 1
fi

# Start the application
echo "Starting the server with enhanced simulations..."
echo "=========================================================================="
python run.py 