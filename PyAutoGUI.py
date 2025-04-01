import pyautogui
import subprocess
import time
import os
import pytesseract
from PIL import Image

class Scanner:
    def __init__(self):
        self.acronis_path = r"C:\Program Files (x86)\Acronis\TrueImageHome\TrueImageLauncher.exe"
    
    def extract_text_from_screenshot(self):
        try:
            image = Image.open("scan_result.png")
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            print(f"Error extracting text from screenshot: {e}")
            return ""

    def scan_file(self, file_path):
        try:
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
            if "Infected" in screenshot_text:
                print("File is infected!")
                return 1 
            else:
                print("File is clean")
                return 0  
                
        except Exception as e:
            print(f"Error during file scan: {e}")
            return -1