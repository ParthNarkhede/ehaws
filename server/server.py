from flask import Flask, request
from datetime import datetime
import os

app = Flask(__name__)

LOG_DIR = "received_logs"
os.makedirs(LOG_DIR, exist_ok=True)

@app.route('/log', methods=['POST'])
def log():
    try:
        log_data = request.form.get('log', '')
        if log_data:
            current_date = datetime.now().strftime("%Y-%m-%d")
            log_file = os.path.join(LOG_DIR, f"logs_{current_date}.txt")
            
            with open(log_file, "a") as f:
                f.write(log_data + "\n")
            
            return "OK", 200
        else:
            return "Empty log", 400
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)  # Disable debug in production!