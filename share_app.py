#!/usr/bin/env python
"""
Rain Investment Platform - Public Access Script
Using localtunnel (no registration required)
"""

import os
import sys
import subprocess
import time
import signal
import socket
import webbrowser
from contextlib import closing
import shutil

def is_port_in_use(port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        return s.connect_ex(('localhost', port)) == 0

def kill_process_on_port(port):
    """Kill any process running on the specified port"""
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
            time.sleep(1)
    except subprocess.CalledProcessError:
        pass

def check_npm_installed():
    """Check if npm is installed"""
    return shutil.which('npm') is not None

def check_lt_installed():
    """Check if localtunnel is installed"""
    return shutil.which('lt') is not None

def install_localtunnel():
    """Install localtunnel"""
    print("Installing localtunnel...")
    try:
        subprocess.run(["npm", "install", "-g", "localtunnel"], check=True)
        print("Localtunnel installed successfully!")
        return True
    except Exception as e:
        print(f"Error installing localtunnel: {e}")
        return False

def print_header():
    print("="*80)
    print("RAIN INVESTMENT PLATFORM - PUBLIC ACCESS")
    print("="*80)
    print("Making your investment platform publicly accessible...")
    print("This script uses localtunnel - a simple alternative to ngrok")
    print("="*80)

def main():
    print_header()
    
    # Default port for the application
    port = 8000
    
    # Check if npm is installed
    if not check_npm_installed():
        print("Error: npm (Node.js package manager) is not installed.")
        print("Please install Node.js from https://nodejs.org/")
        print("Then run this script again.")
        sys.exit(1)
    
    # Check if localtunnel is installed
    if not check_lt_installed():
        print("Localtunnel is not installed.")
        if not install_localtunnel():
            print("Failed to install localtunnel. Please install it manually:")
            print("npm install -g localtunnel")
            sys.exit(1)
    
    # Kill any process on the port
    if is_port_in_use(port):
        print(f"Port {port} is in use. Attempting to free it...")
        kill_process_on_port(port)
    
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
    
    # Start localtunnel
    print("Starting localtunnel to make your application public...")
    lt_process = subprocess.Popen(
        ["lt", "--port", str(port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    
    # Wait for localtunnel to start and get the URL
    time.sleep(3)
    
    # Prepare to read from lt_process stdout to get the URL
    public_url = None
    for i in range(10):  # Try reading a few times
        line = lt_process.stdout.readline().strip()
        if "your url is:" in line.lower():
            public_url = line.split("is:")[-1].strip()
            break
        time.sleep(0.5)
    
    if not public_url:
        print("Failed to get public URL from localtunnel.")
        print("Try running manually: lt --port 8000")
        lt_process.terminate()
        app_process.terminate()
        sys.exit(1)
    
    print("="*80)
    print(f"🎉 Success! Your Rain Investment Platform is now publicly accessible at:")
    print(f"\n🔗 {public_url}\n")
    print("Share this URL with anyone you want to access your investment platform.")
    print("The URL will be valid as long as this script is running.")
    print("="*80)
    
    # Open the public URL in the browser
    webbrowser.open_new_tab(public_url)
    
    print("Press Ctrl+C to stop the server and close the tunnel.")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        # Clean up
        print("Closing localtunnel...")
        lt_process.terminate()
        
        # Kill the application process
        print("Stopping the application...")
        app_process.terminate()
        
        print("="*80)
        print("Your application is no longer publicly accessible.")
        print("Run this script again to make it public again.")
        print("="*80)

if __name__ == "__main__":
    main() 