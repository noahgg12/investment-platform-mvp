#!/bin/bash

echo "========================================================"
echo "Setting up public access for Rain Investment Platform"
echo "Using Serveo.net (No installation required)"
echo "========================================================"

# Kill any existing server
pkill -f uvicorn || true

# Start the application in the background
echo "Starting Rain Investment Platform in the background..."
cd /Users/noah123/BIG\ CODER/investment-platform-mvp
python run.py &

# Wait for the app to start
echo "Waiting for the application to start..."
sleep 5

# Use serveo.net to create a tunnel
echo "Creating a public tunnel using serveo.net..."
echo "Your application will be available at the URL shown below:"
echo "========================================================"
echo "Press Ctrl+C to stop the server and close the tunnel."

# Connect to serveo.net and forward port 8000
ssh -R 80:localhost:8000 serveo.net

# When the user presses Ctrl+C, stop the server
echo "Shutting down the application..."
pkill -f uvicorn

echo "========================================================"
echo "Your application is no longer publicly accessible."
echo "Run this script again to make it public again."
echo "========================================================" 