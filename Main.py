from flask import Flask, request, jsonify
from BackGUI import BackupManager
from PyAutoGUI import Scanner
import os

app = Flask(__name__)

backup_manager = BackupManager()
scan_manager = Scanner()

@app.route('/backup', methods=['POST'])
def backup():
    data = request.get_json()
    source = data.get('source')
    destination = data.get('destination')

    if not source or not destination:
        return jsonify({'status': 'error', 'message': 'Source and destination paths are required'}), 400

    if not os.path.exists(source):
        return jsonify({'status': 'error', 'message': f'Source path does not exist: {source}'}), 400
        
    os.makedirs(os.path.dirname(destination), exist_ok=True)

    result = backup_manager.start_backup(source, destination)

    return jsonify({'status': 'success' if "successfully" in result else 'error', 'message': result})

@app.route('/scan', methods=['POST'])
def scan():
    if request.is_json:
        data = request.get_json()
        file_path = data.get('file_path')
        
        if not file_path or not os.path.exists(file_path):
            return jsonify({'status': 'error', 'message': 'Invalid file path'}), 400
            
        result = scan_manager.scan_file(file_path)
    
    elif 'file' in request.files:
        file = request.files['file']
        file_path = f"./{file.filename}"
        file.save(file_path)
        
        result = scan_manager.scan_file(file_path)
        
        try:
            os.remove(file_path)
        except:
            pass
    else:
        return jsonify({'status': 'error', 'message': 'No file or file path provided'}), 400

    return jsonify({'status': 'Infected' if result == 1 else 'Clean' if result == 0 else 'Error', 'message': 'Scan complete'})

@app.route('/get-coordinates', methods=['GET'])
def get_coordinates():
    pos = backup_manager.get_coordinates()
    return jsonify(pos), 200

@app.route('/status', methods=['GET'])
def status():
    return jsonify({'status': 'running', 'message': 'API is up and running'})


if __name__ == '__main__':
    print("Starting API server...")
    print("Available endpoints:")
    print("  POST /backup - Start a backup operation")
    print("  POST /scan - Scan a file for viruses")
    print("  GET /get-coordinates - Helper to find screen coordinates")
    print("  GET /status - Check API status")
    app.run(debug=True)
