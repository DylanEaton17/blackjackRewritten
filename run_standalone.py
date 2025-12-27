#!/usr/bin/env python3
"""
Standalone launcher for Blackjack Web Application
Automatically opens browser and runs Flask server
"""
import webbrowser
import threading
import time
import sys
import os

# Add the directory containing the executable to the path
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    application_path = sys._MEIPASS
else:
    # Running as script
    application_path = os.path.dirname(os.path.abspath(__file__))

# Import Flask app
from app import app

def open_browser():
    """Open browser after short delay to ensure server is ready"""
    time.sleep(1.5)
    webbrowser.open('http://127.0.0.1:5000/')

if __name__ == '__main__':
    print("=" * 60)
    print("  Blackjack Story Mode - Standalone Edition")
    print("=" * 60)
    print("\nStarting server...")
    print("The game will open in your browser automatically.")
    print("\nTo stop the server, press Ctrl+C in this window.")
    print("=" * 60)
    
    # Open browser in separate thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run Flask app
    try:
        app.run(host='127.0.0.1', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
        print("Thanks for playing!")
