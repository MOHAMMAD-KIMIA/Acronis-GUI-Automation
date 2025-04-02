import pyautogui
import subprocess
import time
import os
import pytesseract
import logging
from PIL import Image

class Scanner:
    def __init__(self):
        self.acronis_path = r"C:\Program Files (x86)\Acronis\TrueImageHome\TrueImageLauncher.exe"
        self.history = [] 

        logging.basicConfig(
            filename="scan_log.txt", 
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        logging.info("Scanner initialized.")

    def extract_text_from_screenshot(self):
        try:
            image = Image.open("scan_result.png")
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            logging.error(f"Error extracting text from screenshot: {e}")
            return ""

    def scan_file(self, file_path):
        try:
            logging.info(f"Starting scan for file: {file_path}")

            print("Launching Acronis TrueImage for scanning...")
            subprocess.Popen(self.acronis_path)
            time.sleep(5)

            print("Selecting file for scan...")
            pyautogui.click(500, 500)
            time.sleep(1)
            pyautogui.write(file_path)
            pyautogui.press('enter')
            time.sleep(1)

            print("Starting scan...")
            pyautogui.click(600, 600)
            time.sleep(5)

            screenshot = pyautogui.screenshot()
            screenshot.save("scan_result.png")

            screenshot_text = self.extract_text_from_screenshot()
            result = "Infected" if "Infected" in screenshot_text else "Clean"

            self.history.append({'file': file_path, 'result': result})
            logging.info(f"Scan completed: {file_path} - {result}")

            print(f"Scan completed. File is {result}")
            return 1 if result == "Infected" else 0

        except Exception as e:
            logging.error(f"Error during file scan: {e}")
            return -1

    def load_scan_history(self):
        logging.info("Loading scan history.")
        return self.history  