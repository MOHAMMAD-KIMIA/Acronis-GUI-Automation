# **Acronis GUI Automation API**  

Acronis GUI Automation API is a **Flask-based automation tool** that enables users to interact with **Acronis TrueImage** for backup and file scanning operations through a **REST API**. The project uses **PyAutoGUI** for GUI automation, **pytesseract** for text extraction from screenshots, and **logging** to track all operations.

This tool is useful when **Acronis TrueImage does not provide a command-line interface (CLI) or API** and you need an automated way to interact with its GUI.

---

## ** Features**  
✅ **Automated File Backup**: Start a backup process by specifying the source and destination directories.  
✅ **Automated File Scanning**: Scan a file for potential threats using Acronis TrueImage.  
✅ **Retrieve Scan History**: Get a list of previously scanned files along with their results.  
✅ **Mouse Coordinate Helper**: Identify screen coordinates to fine-tune PyAutoGUI operations.  
✅ **API Status Check**: Verify whether the API is running.  
✅ **Logging System**: All operations (backups, scans, errors) are recorded in `log.txt`.  

---

## ** Installation**  

### **🔹 1. Clone the Repository**  
First, clone the repository and navigate into the project directory:  
```bash
git clone https://github.com/yourusername/Acronis-GUI-Automation.git
cd Acronis-GUI-Automation
```

### **🔹 2. Install Dependencies**  
Install the required Python packages using:  
```bash
pip install -r requirements.txt
```

### **🔹 3. Run the Flask API**  
Once the dependencies are installed, start the API server by running:  
```bash
python Main.py
```
After running the command, you should see output similar to:  
```
Starting API server...
  POST /backup - Start a backup operation
  POST /scan - Scan a file for viruses
  GET /get-coordinates - Helper to find screen coordinates
  GET /scan/history - Retrieve scan history
  GET /status - Check API status
```
This means the API is up and running at `http://127.0.0.1:5000/`.

---

## ** API Endpoints and Usage**  

Below are the available API endpoints and how to use them via **PowerShell**.

### **🔹 1. Start a File Scan**
**Endpoint:** `POST /scan`  
**Description:** Scans a file for viruses using Acronis TrueImage.  
**PowerShell Command:**  
```powershell
& curl.exe -X POST -F "file=@C:/Users/LOQ/Desktop/TestToScan.exe" http://127.0.0.1:5000/scan
```
**Response Example:**  
```json
{
    "status": "success",
    "message": "Scan completed. No threats found."
}
```
or if an issue is found:
```json
{
    "status": "warning",
    "message": "Threat detected in file!"
}
```

---

### **🔹 2. Retrieve Scan History**
**Endpoint:** `GET /scan/history`  
**Description:** Returns a list of scanned files and their results.  
**PowerShell Command:**  
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/scan/history" -Method Get
```
**Response Example:**  
```json
{
    "history": [
        {
            "file": "C:/Users/LOQ/Desktop/TestToScan.exe",
            "result": "Clean"
        },
        {
            "file": "C:/Users/LOQ/Desktop/Malware.exe",
            "result": "Infected"
        }
    ]
}
```

---

### **🔹 3. Start a Backup Operation**
**Endpoint:** `POST /backup`  
**Description:** Initiates a backup from a specified source directory to a destination.  
**PowerShell Command:**  
```powershell
curl -X POST http://127.0.0.1:5000/backup -H "Content-Type: application/json" -d "{\"source\": \"D:\\University\\Term 6\\testfolder\", \"destination\": \"G:\\Newfolder\"}"
```
**Response Example:**  
```json
{
    "status": "success",
    "message": "Backup started successfully"
}
```

---

### **🔹 4. Get Mouse Coordinates**
**Endpoint:** `GET /get-coordinates`  
**Description:** A helper function to get the current mouse cursor position.  
**PowerShell Command:**  
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/get-coordinates" -Method Get
```
**Response Example:**  
```json
{
    "x": 1023,
    "y": 345
}
```
This helps in fine-tuning PyAutoGUI's automation process.

---

### **🔹 5. Check API Status**
**Endpoint:** `GET /status`  
**Description:** Checks if the API is running.  
**PowerShell Command:**  
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/status" -Method Get
```
**Response Example:**  
```json
{
    "status": "running",
    "message": "API is up and running"
}
```

---

## ** Logging System**  

All backup and scanning operations, along with errors, are logged in **`log.txt`**. This helps with debugging and monitoring.

### **🔹 Example Log Entries**
```
[2025-04-02 19:30:12] INFO: Backup started from D:\University\Term 6\testfolder to G:\Newfolder
[2025-04-02 19:31:20] INFO: Scan started for file C:/Users/LOQ/Desktop/TestToScan.exe
[2025-04-02 19:31:25] ERROR: Scan failed due to missing Acronis application
```
Each log entry contains a **timestamp**, **log level (INFO/ERROR)**, and a **description** of the operation.

---

## ** Troubleshooting**  

**1. Acronis TrueImage is not opening automatically?**  
- Ensure Acronis is installed at:  
  `C:\Program Files (x86)\Acronis\TrueImageHome\TrueImageLauncher.exe`  
- Try opening Acronis manually and check for errors.

**2. PyAutoGUI is not clicking the right elements?**  
- Use the `/get-coordinates` endpoint to determine the correct screen coordinates.  
- Adjust the **click positions** in the Python code.

**3. Tesseract OCR is not detecting text?**  
- Install **Tesseract OCR** and ensure it’s added to the system `PATH`.  
- Try using different OCR configurations.

---

## ** How It Works Internally**  

1. **BackupManager (BackGUI.py)**  
   - Automates Acronis backup operations by simulating user interactions.  
   - Uses **PyAutoGUI** to click and type paths in the GUI.  
   - Takes screenshots of the backup result.

2. **Scanner (PyAutoGUI.py)**  
   - Automates Acronis virus scanning.  
   - Extracts scan results using **pytesseract** (OCR).  
   - Saves scan history.

3. **Flask API (Main.py)**  
   - Provides a REST API for backup and scanning.  
   - Routes user requests to the **BackupManager** and **Scanner** classes.

---

## ** License**  
This project is licensed under the **MIT License**. You are free to modify and distribute it.  
