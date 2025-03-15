#!/bin/bash

# Navigate to the project directory
cd "$(dirname "$0")"

echo "========================================================"
echo "RESTARTING INVESTMENT PLATFORM (FIXING SERVER ERROR)"
echo "========================================================"

# Kill any existing uvicorn processes
echo "Stopping any running servers..."
pkill -9 -f uvicorn

# Make sure all Python processes related to the app are terminated
echo "Ensuring no lingering Python processes..."
ps aux | grep "python run.py" | grep -v grep | awk '{print $2}' | xargs -I {} kill -9 {} 2>/dev/null

# Wait a moment for processes to terminate
sleep 2

# Check if port 8000 is in use
if lsof -i :8000 > /dev/null 2>&1; then
    echo "Port 8000 is still in use. Forcefully terminating processes..."
    lsof -i :8000 -t | xargs kill -9 2>/dev/null
    sleep 1
fi

# Start the application with error handling
echo "Starting the fixed server..."
echo "========================================================"
python run.py

# Check if server started successfully
if [ $? -ne 0 ]; then
    echo "========================================================"
    echo "ERROR: Server failed to start. Please check the logs above."
    echo "If you see 'Address already in use', try running:"
    echo "lsof -i :8000 -t | xargs kill -9"
    echo "Then run this script again."
    echo "========================================================"
    exit 1
fi 