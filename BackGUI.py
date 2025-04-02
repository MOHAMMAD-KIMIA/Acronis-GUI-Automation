import pyautogui
import subprocess
import time
import os
import logging

logging.basicConfig(
    filename="log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class BackupManager:
    def __init__(self):
        self.acronis_path = r"C:\Program Files (x86)\Acronis\TrueImageHome\TrueImageLauncher.exe"
    
    def start_backup(self, source_path, destination_path):
        try:
            logging.info("Launching Acronis TrueImage...")
            subprocess.Popen(self.acronis_path)
            time.sleep(5)

            logging.info("Clicking backup button...")
            pyautogui.click(26, 52)
            time.sleep(2)

            logging.info("Selecting source...")
            pyautogui.click(1023, 345)
            time.sleep(1)
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.write(source_path)
            pyautogui.press('enter')
            time.sleep(2)

            logging.info("Selecting destination...")
            pyautogui.click(1502, 372)
            time.sleep(1)
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.write(destination_path)
            pyautogui.press('enter')
            time.sleep(2)

            logging.info("Starting backup...")
            pyautogui.click(1805, 1003)
            time.sleep(2)

            screenshot = pyautogui.screenshot()
            screenshot.save("backup_result.png")
            logging.info("Backup initiated successfully.")
            
            return "Backup started successfully"
            
        except Exception as e:
            logging.error(f"Error during backup process: {e}")
            return f"Error during backup: {str(e)}"
    
    def get_coordinates(self):
        logging.info("Waiting 5 seconds for user to place the mouse over the target element...")
        time.sleep(5)
        pos = pyautogui.position()
        logging.info(f"Mouse position recorded: x={pos.x}, y={pos.y}")
        return {'x': pos.x, 'y': pos.y}