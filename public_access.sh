#!/bin/bash

echo "========================================================"
echo "Setting up public access for Rain Investment Platform"
echo "========================================================"

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "ngrok not found. Installing ngrok..."
    
    # Check if Homebrew is installed
    if command -v brew &> /dev/null; then
        echo "Installing ngrok using Homebrew..."
        brew install ngrok
    else
        echo "Homebrew not found. Installing ngrok manually..."
        
        # Create a temporary directory for the download
        TEMP_DIR=$(mktemp -d)
        cd $TEMP_DIR
        
        # Download ngrok
        echo "Downloading ngrok..."
        curl -O https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-darwin-amd64.zip
        
        # Unzip ngrok
        echo "Extracting ngrok..."
        unzip ngrok-v3-stable-darwin-amd64.zip
        
        # Move ngrok to a location in PATH
        echo "Installing ngrok..."
        chmod +x ngrok
        sudo mv ngrok /usr/local/bin/
        
        # Clean up
        cd -
        rm -rf $TEMP_DIR
    fi
    
    echo "ngrok installation complete!"
    echo "You'll need to sign up for a free ngrok account at https://ngrok.com/"
    echo "After signing up, you'll get an authtoken to configure ngrok."
    echo "Run: ngrok config add-authtoken YOUR_TOKEN"
    read -p "Press Enter to continue after you've configured your authtoken..." 
fi

echo "Starting Rain Investment Platform in the background..."
cd /Users/noah123/BIG\ CODER/investment-platform-mvp
pkill -f uvicorn || true
python run.py &

# Wait for the application to start
echo "Waiting for the application to start..."
sleep 5

# Start ngrok
echo "Starting ngrok tunnel to make the application publicly accessible..."
echo "Your application will be available at the 'Forwarding' URL shown below:"
echo "========================================================"
ngrok http 8000

# Note: This will keep running until the user presses Ctrl+C
# When they exit ngrok, we should also stop the FastAPI application
echo "Shutting down the application..."
pkill -f uvicorn

echo "========================================================"
echo "Your application is no longer publicly accessible."
echo "Run this script again to make it public again."
echo "========================================================" 