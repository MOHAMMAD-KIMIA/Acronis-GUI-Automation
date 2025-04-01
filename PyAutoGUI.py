import pyautogui
import subprocess
import time
import pytesseract
import json
from PIL import Image
from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

HISTORY_FILE = "scan_history.json"

def extract_text_from_screenshot():
    try:
        image = Image.open("scan_result.png")
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Error extracting text from screenshot: {e}")
        return ""

def scan_file_with_gui(file_path):
    acronis_path = r"C:\Program Files (x86)\Acronis\TrueImageHome\TrueImageLauncher.exe"
    try:
        subprocess.Popen(acronis_path)
        time.sleep(5)
        pyautogui.click(500, 500)
        time.sleep(1)
        pyautogui.write(file_path)
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.click(600, 600)
        time.sleep(5)
        
        screenshot = pyautogui.screenshot()
        screenshot.save("scan_result.png")
        
        screenshot_text = extract_text_from_screenshot()
        return 1 if "Infected" in screenshot_text else 0
    except Exception as e:
        print(f"Error during file scan: {e}")
        return -1

def save_scan_result(file_name, status):
    scan_data = {
        "file": file_name,
        "status": "Infected" if status == 1 else "Clean",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []
    else:
        history = []

    history.append(scan_data)

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

@app.route('/scan', methods=['POST'])
def scan():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    file_path = f"./{file.filename}"
    file.save(file_path)

    result = scan_file_with_gui(file_path)
    
    if result == 1:
        status = "Infected"
    elif result == 0:
        status = "Clean"
    else:
        return jsonify({'status': 'Error during scanning'}), 500

    save_scan_result(file.filename, result)

    return jsonify({'status': status}), 200

@app.route('/scan-history', methods=['GET'])
def get_scan_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []
    else:
        history = []

    return jsonify({"scan_history": history})

if __name__ == '__main__':
    app.run(debug=True)