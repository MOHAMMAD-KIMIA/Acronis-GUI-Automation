import pyautogui
import subprocess
import time
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

def backup_with_gui(source_path, destination_path):
    acronis_path = r"C:\Program Files (x86)\Acronis\TrueImageHome\TrueImageLauncher.exe"
    try:
        print("Launching Acronis TrueImage...")
        subprocess.Popen(acronis_path)
        time.sleep(5)

        print("Clicking backup button...")
        pyautogui.click(1441, 469)
        time.sleep(2)

        print("Selecting source...")
        pyautogui.click(998, 361)
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write(source_path)
        pyautogui.press('enter')
        time.sleep(2)

        print("Selecting destination...")
        pyautogui.click(1537, 465)
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write(destination_path)
        pyautogui.press('enter')
        time.sleep(2)

        print("Starting backup...")
        pyautogui.click(1813, 997)
        time.sleep(2)

        screenshot = pyautogui.screenshot()
        screenshot.save("backup_result.png")
        print("Backup initiated successfully")
        
        return "Backup started successfully"
        
    except Exception as e:
        print(f"Error during backup process: {e}")
        return f"Error during backup: {str(e)}"

@app.route('/backup', methods=['POST'])
def backup():
    data = request.get_json()
    
    if not data or 'source' not in data or 'destination' not in data:
        return jsonify({'status': 'error', 'message': 'Source and destination paths are required'}), 400
    
    source_path = data['source']
    destination_path = data['destination']

    if not os.path.exists(source_path):
        return jsonify({'status': 'error', 'message': f'Source path does not exist: {source_path}'}), 400

    os.makedirs(os.path.dirname(destination_path), exist_ok=True)
    
    result = backup_with_gui(source_path, destination_path)
    
    if "successfully" in result:
        return jsonify({'status': 'success', 'message': result}), 200
    else:
        return jsonify({'status': 'error', 'message': result}), 500

@app.route('/get-coordinates', methods=['GET'])
def get_coordinates():
    print("Position your mouse over the target element and wait 5 seconds...")
    time.sleep(5)
    pos = pyautogui.position()
    return jsonify({'x': pos.x, 'y': pos.y}), 200

if __name__ == '__main__':
    print("Starting Acronis Backup API server...")
    # print("Available endpoints:")
    # print("  POST /backup - Start a backup operation")
    # print("  GET /get-coordinates - Helper to find screen coordinates")
    app.run(debug=True) 