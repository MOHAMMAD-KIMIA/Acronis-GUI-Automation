import pyautogui
import subprocess
import time
import threading
import pytesseract
from PIL import Image
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

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

@app.route('/scan', methods=['POST'])
def scan():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    file_path = f"./{file.filename}"
    file.save(file_path)
    
    result = scan_file_with_gui(file_path)
    
    if result == 1:
        return jsonify({'status': 'Infected'}), 200
    elif result == 0:
        return jsonify({'status': 'Clean'}), 200
    else:
        return jsonify({'status': 'Error during scanning'}), 500

if __name__ == '__main__':
    app.run(debug=True)