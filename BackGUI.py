import pyautogui
import subprocess
import time
import os

class BackupManager:
    def __init__(self):
        self.acronis_path = r"C:\Program Files (x86)\Acronis\TrueImageHome\TrueImageLauncher.exe"
    
    def start_backup(self, source_path, destination_path):
        try:
            print("Launching Acronis TrueImage...")
            subprocess.Popen(self.acronis_path)
            time.sleep(5)

            print("Clicking backup button...")
            pyautogui.click(26, 52)
            time.sleep(2)

            print("Selecting source...")
            pyautogui.click(1023, 345)
            time.sleep(1)
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.write(source_path)
            pyautogui.press('enter')
            time.sleep(2)

            print("Selecting destination...")
            pyautogui.click(1502, 372)
            time.sleep(1)
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.write(destination_path)
            pyautogui.press('enter')
            time.sleep(2)

            print("Starting backup...")
            pyautogui.click(1805, 1003)
            time.sleep(2)

            screenshot = pyautogui.screenshot()
            screenshot.save("backup_result.png")
            print("Backup initiated successfully")
            
            return "Backup started successfully"
            
        except Exception as e:
            print(f"Error during backup process: {e}")
            return f"Error during backup: {str(e)}"
    
    def get_coordinates(self):
        print("Position your mouse over the target element and wait 5 seconds...")
        time.sleep(5)
        pos = pyautogui.position()
        return {'x': pos.x, 'y': pos.y}