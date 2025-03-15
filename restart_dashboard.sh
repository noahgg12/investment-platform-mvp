#!/bin/bash

# Script to restart the server with dashboard functionality

echo "=========================================================="
echo "RESTARTING SERVER WITH DASHBOARD FUNCTIONALITY"
echo "=========================================================="

# Navigate to the project directory
cd "$(dirname "$0")"

# Kill any running server processes
echo "Stopping any running servers..."
pkill -9 -f uvicorn 2>/dev/null || true
ps aux | grep "python run.py" | grep -v grep | awk '{print $2}' | xargs -I{} kill -9 {} 2>/dev/null || true

# Free up port 8000
if command -v lsof >/dev/null 2>&1; then
    lsof -i :8000 -t | xargs kill -9 2>/dev/null || true
fi

# Wait for port to be completely free
echo "Waiting for port to be freed..."
sleep 2

# Start the server
echo "Starting server with dashboard functionality..."
echo "=========================================================="

# Start the server and open the dashboard in the browser
python -c "
import webbrowser
import threading
import time

def open_dashboard():
    time.sleep(2)  # Wait for the server to start
    webbrowser.open('http://localhost:8000/dashboard')

threading.Thread(target=open_dashboard).start()
" &

# Start the server
python run.py

echo "Server started with dashboard functionality!" 