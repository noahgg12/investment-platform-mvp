#!/usr/bin/env python
"""
Rain Investment Platform - Public Access Script

This script starts the Rain Investment Platform and makes it publicly accessible
using ngrok. It provides a programmatic alternative to the shell script.
"""

import os
import sys
import subprocess
import time
import signal
import socket
import webbrowser
from pyngrok import ngrok, conf
from contextlib import closing

def is_port_in_use(port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        return s.connect_ex(('localhost', port)) == 0

def kill_process_on_port(port):
    """Kill any process running on the specified port"""
    # This works on macOS and Linux
    try:
        output = subprocess.check_output(f"lsof -i :{port} -t", shell=True).decode().strip()
        if output:
            pids = output.split('\n')
            for pid in pids:
                try:
                    os.kill(int(pid), signal.SIGKILL)
                    print(f"Killed process {pid} running on port {port}")
                except:
                    pass
            # Wait a moment for the port to be released
            time.sleep(1)
    except subprocess.CalledProcessError:
        # No process found on this port
        pass

def print_header():
    print("="*80)
    print("RAIN INVESTMENT PLATFORM - PUBLIC ACCESS")
    print("="*80)
    print("Making your investment platform publicly accessible...")

def setup_ngrok():
    """Set up and configure ngrok"""
    # Check if ngrok auth token is set
    if not conf.get_default().auth_token:
        print("ngrok auth token not found.")
        print("You need to sign up for a free account at https://ngrok.com/ and get your auth token.")
        print("Then set it with: ngrok config add-authtoken YOUR_TOKEN")
        token = input("Enter your ngrok auth token (or press Enter to exit): ")
        if not token:
            print("Exiting...")
            sys.exit(1)
        conf.get_default().auth_token = token

def main():
    print_header()
    
    # Default port for the application
    port = 8000
    
    # Set up ngrok
    setup_ngrok()
    
    # Kill any process on the port
    if is_port_in_use(port):
        print(f"Port {port} is in use. Attempting to free it...")
        kill_process_on_port(port)
    
    # If port is still in use, we'll force it to close
    if is_port_in_use(port):
        print(f"Port {port} is still in use. Please close any applications using this port.")
        print("You can do this by running: pkill -f uvicorn")
        sys.exit(1)
    
    # Start the application in a separate process
    print("Starting Rain Investment Platform...")
    app_process = subprocess.Popen(
        ["python", "run.py"], 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    
    # Wait for the application to start
    print("Waiting for the application to start...")
    time.sleep(5)
    
    # Check if the application started successfully
    if app_process.poll() is not None:
        print("Failed to start the application. Check the error messages:")
        print(app_process.stderr.read())
        sys.exit(1)
    
    # Start ngrok tunnel
    print("Starting ngrok tunnel...")
    try:
        # Open an HTTP tunnel on the default port
        public_url = ngrok.connect(port).public_url
        
        print("="*80)
        print(f"🎉 Success! Your Rain Investment Platform is now publicly accessible at:")
        print(f"\n🔗 {public_url}\n")
        print("Share this URL with anyone you want to access your investment platform.")
        print("The URL will be valid as long as this script is running.")
        print("="*80)
        
        # Open the public URL in the browser
        webbrowser.open_new_tab(public_url)
        
        print("Press Ctrl+C to stop the server and close the tunnel.")
        
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        # Clean up
        print("Closing ngrok tunnel...")
        ngrok.kill()
        
        # Kill the application process
        print("Stopping the application...")
        app_process.terminate()
        app_process.wait()
        
        print("="*80)
        print("Your application is no longer publicly accessible.")
        print("Run this script again to make it public again.")
        print("="*80)

if __name__ == "__main__":
    main() 