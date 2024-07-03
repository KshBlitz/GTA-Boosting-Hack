import cv2
import numpy as np
import pyautogui
import pytesseract
from time import sleep

# Tesseract OCR path configuration if needed
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\mahaj\tesseract.exe'

# List of specific numbers to find
target_numbers = ["12", "34", "56"]  # Add your specific numbers here

# Function to capture the screen
def capture_screen():
    screenshot = pyautogui.screenshot()
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    return frame

# Function to find and highlight specific numbers in the frame
def find_numbers(frame, target_numbers):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Use adaptive thresholding to improve OCR accuracy
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    data = pytesseract.image_to_data(thresh, output_type=pytesseract.Output.DICT)
    n_boxes = len(data['text'])

    for i in range(n_boxes):
        if int(data['conf'][i]) > 60:  # Confidence threshold
            text = data['text'][i]
            if text in target_numbers:
                (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    return frame

while True:
    frame = capture_screen()
    highlighted_frame = find_numbers(frame, target_numbers)
    cv2.imshow('Number Finder', highlighted_frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    sleep(0.1)  # Adjust the delay to match the refresh rate of the numbers on your screen

cv2.destroyAllWindows()
