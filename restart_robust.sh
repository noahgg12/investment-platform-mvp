#!/bin/bash

# Exit on any error
set -e

# Get the absolute path to the project directory
PROJECT_DIR="/Users/noah123/BIG CODER/investment-platform-mvp"
cd "$PROJECT_DIR"

echo "========================================================"
echo "ROBUST SERVER RESTART - FIXING ALL ISSUES"
echo "========================================================"
echo "Project directory: $PROJECT_DIR"

# Kill everything brutally
echo "Aggressively killing all related processes..."

# Kill uvicorn and python processes
echo "Killing uvicorn processes..."
pkill -9 -f uvicorn 2>/dev/null || true

echo "Killing Python processes related to the app..."
pkill -9 -f "python run.py" 2>/dev/null || true
pkill -9 -f "app.main:app" 2>/dev/null || true

# Clean up any processes using port 8000
echo "Clearing port 8000..."
if command -v lsof >/dev/null 2>&1; then
    PIDS=$(lsof -i :8000 -t 2>/dev/null)
    if [ -n "$PIDS" ]; then
        echo "Found processes using port 8000: $PIDS"
        for PID in $PIDS; do
            echo "Killing process $PID"
            kill -9 $PID 2>/dev/null || true
        done
    else
        echo "No processes found using port 8000"
    fi
else
    echo "lsof not available, trying alternative method"
    # Alternative method for finding processes using port 8000
    if command -v netstat >/dev/null 2>&1; then
        echo "Using netstat to find processes on port 8000"
        PIDS=$(netstat -anv | grep LISTEN | grep ".8000" | awk '{print $9}' 2>/dev/null)
        if [ -n "$PIDS" ]; then
            echo "Found processes: $PIDS"
            for PID in $PIDS; do
                echo "Killing process $PID"
                kill -9 $PID 2>/dev/null || true
            done
        fi
    fi
fi

# Ensure the port is really free
echo "Waiting for port 8000 to be free..."
sleep 3

# Check if port is still in use after wait
if command -v lsof >/dev/null 2>&1; then
    if lsof -i :8000 >/dev/null 2>&1; then
        echo "WARNING: Port 8000 is still in use. Attempting more aggressive measures..."
        lsof -i :8000 -t | xargs kill -9 2>/dev/null || true
        sleep 2
    fi
fi

# Verify templates directory exists
if [ ! -d "$PROJECT_DIR/templates" ]; then
    echo "ERROR: Templates directory not found at $PROJECT_DIR/templates"
    echo "Please make sure you're in the correct project directory"
    exit 1
fi

# Verify run.py exists
if [ ! -f "$PROJECT_DIR/run.py" ]; then
    echo "ERROR: run.py not found at $PROJECT_DIR/run.py"
    echo "Creating basic run.py file..."
    
    cat > "$PROJECT_DIR/run.py" << 'EOF'
#!/usr/bin/env python3
"""
Run script for the AI Investment Platform
"""

import os
import sys
import webbrowser
from threading import Timer

def open_browser():
    webbrowser.open('http://localhost:8000')

if __name__ == "__main__":
    print("=" * 80)
    print("STARTING AI INVESTMENT PLATFORM")
    print("=" * 80)
    print("Make sure you have installed all required packages with:")
    print("pip install -r requirements.txt")
    
    # Try to import uvicorn to check if dependencies are installed
    try:
        import uvicorn
    except ImportError:
        print("\nERROR: uvicorn not found. Please install the requirements:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    
    # Check for port in use and force free it
    try:
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('0.0.0.0', 8000))
    except socket.error:
        print("Port 8000 is in use. Attempting to free it...")
        if sys.platform.startswith('darwin') or sys.platform.startswith('linux'):
            try:
                os.system("lsof -i :8000 -t | xargs kill -9")
                print("Killed processes running on port 8000")
            except:
                print("Failed to kill processes. Please free port 8000 manually.")
                sys.exit(1)
    
    print("Opening browser at: http://localhost:8000")
    print("Press Ctrl+C to stop the server")
    print("=" * 80)
    
    # Open the browser after the server starts
    Timer(2, open_browser).start()
    
    # Start the server
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
EOF
    
    chmod +x "$PROJECT_DIR/run.py"
fi

# Clear any Python cache to ensure clean start
echo "Clearing Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} +  2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true

# Start the application
echo "Starting the application with robust error handling..."
echo "========================================================"
python run.py

# This will only execute if the previous command fails
echo "========================================================"
echo "ERROR: Failed to start the server"
echo "If you see 'Address already in use', try manually killing processes:"
echo "  lsof -i :8000 -t | xargs kill -9"
echo "Then run this script again."
echo "========================================================"
exit 1 