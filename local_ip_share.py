#!/usr/bin/env python
"""
Rain Investment Platform - Local Network Sharing

This script starts the application and makes it accessible on your local network.
Other people on the same network (like home or office WiFi) can access it.
"""

import os
import sys
import subprocess
import time
import signal
import socket
from contextlib import closing
import webbrowser

def get_local_ip():
    """Get the local IP address of this machine"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

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

def print_header():
    print("="*80)
    print("RAIN INVESTMENT PLATFORM - LOCAL NETWORK SHARING")
    print("="*80)
    print("Making your investment platform accessible on your local network...")
    print("People on the same WiFi/network can access your application.")
    print("="*80)

def main():
    print_header()
    
    # Default port for the application
    port = 8000
    
    # Get local IP address
    local_ip = get_local_ip()
    
    # Kill any process on the port
    if is_port_in_use(port):
        print(f"Port {port} is in use. Attempting to free it...")
        kill_process_on_port(port)
    
    # Modify run.py to listen on all interfaces
    # This is required for the app to be accessible from other devices
    print(f"Starting Rain Investment Platform on {local_ip}:{port}...")
    
    # Use a custom command to start the application with the right host
    app_process = subprocess.Popen(
        ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", str(port), "--reload"],
        cwd="/Users/noah123/BIG CODER/investment-platform-mvp"
    )
    
    # Wait for the application to start
    time.sleep(3)
    
    # Show the sharing info
    print("="*80)
    print(f"🎉 Success! Your Rain Investment Platform is now accessible at:")
    print(f"\n🔗 http://{local_ip}:{port}\n")
    print("People on your local network can access your platform using this address.")
    print("Note: This only works for people on the same network as you.")
    print("="*80)
    print("You can access it on this device at: http://localhost:8000")
    print("="*80)
    
    # Open the local URL in the browser
    webbrowser.open_new_tab(f"http://localhost:{port}")
    
    print("Press Ctrl+C to stop the server...")
    
    try:
        # Keep the script running
        app_process.wait()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        # Kill the application process
        print("Stopping the application...")
        app_process.terminate()
        
        print("="*80)
        print("Your application is no longer accessible.")
        print("="*80)

if __name__ == "__main__":
    main() 