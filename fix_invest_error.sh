#!/bin/bash

# Ultra-aggressive script to fix the 500 error on the invest endpoint

echo "========================================================"
echo "FIXING INTERNAL SERVER ERROR ON INVESTMENT PLATFORM"
echo "========================================================"

# Force kill everything
echo "Killing all processes..."
pkill -9 -f uvicorn 2>/dev/null || true
pkill -9 -f "python run.py" 2>/dev/null || true
pkill -9 -f "app.main:app" 2>/dev/null || true

# Use lsof to find and kill any process on port 8000
echo "Freeing port 8000..."
if command -v lsof >/dev/null 2>&1; then
    lsof -i :8000 -t | xargs kill -9 2>/dev/null || true
fi

# Make sure port 8000 is completely free
echo "Ensuring port is completely free..."
sleep 2

# Navigate to the project directory
cd "$(dirname "$0")"

# Clear Python cache
echo "Removing Python cache files..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true

# Create fresh run file
echo "Creating a fresh run file..."
cat > run.py << 'EOF'
#!/usr/bin/env python3
"""
Debug version of run script for the AI Investment Platform
"""

import os
import sys
import webbrowser
from threading import Timer
import logging

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("run")

def open_browser():
    webbrowser.open('http://localhost:8000')

if __name__ == "__main__":
    print("=" * 80)
    print("STARTING AI INVESTMENT PLATFORM (DEBUG MODE)")
    print("=" * 80)
    print("Make sure you have installed all required packages with:")
    print("pip install -r requirements.txt")
    
    # Try to import required packages
    try:
        import uvicorn
        import fastapi
        import numpy
        import jinja2
    except ImportError as e:
        print(f"\nERROR: Missing dependency: {e}")
        print("Please install the requirements:")
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
    
    # Use extra debug options
    os.environ["PYTHONUNBUFFERED"] = "1"  # Ensure unbuffered output
    
    # Start the server in debug mode
    import uvicorn
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True, 
        workers=1,  # Use only 1 worker for debugging
        log_level="debug"
    )
EOF

# Make the run file executable
chmod +x run.py

echo "========================================================"
echo "STARTING SERVER IN DEBUG MODE - FIX FOR INVEST ENDPOINT"
echo "========================================================"
python run.py 