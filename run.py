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
