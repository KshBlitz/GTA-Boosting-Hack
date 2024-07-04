import cv2
import numpy as np
import pyautogui
import pytesseract
from time import sleep
import tkinter as tk
from tkinter import simpledialog

# Tesseract OCR path configuration if needed
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\mahaj\tesseract.exe'

# Function to capture the screen
def capture_screen():
    screenshot = pyautogui.screenshot()
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    return frame

# Function to crop the frame to the lower 60% of the screen and central 50% in width
def crop_focus_area(frame):
    height, width, _ = frame.shape
    start_x = int(width * 0.25)
    end_x = int(width * 0.75)
    start_y = int(height * 0.4)
    end_y = height
    return frame[start_y:end_y, start_x:end_x]

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

# Function to take 6 two-digit numbers input from user using tkinter
def get_user_numbers():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    while True:
        user_input = simpledialog.askstring("Input", "Enter 6 two-digit numbers separated by space:")
        if user_input:
            numbers = user_input.split()
            if len(numbers) == 6 and all(num.isdigit() and len(num) == 2 for num in numbers):
                root.destroy()
                return numbers
            else:
                tk.messagebox.showerror("Invalid input", "Please enter exactly 6 two-digit numbers.")
        else:
            tk.messagebox.showerror("Invalid input", "Input cannot be empty.")

# Main code
target_numbers = get_user_numbers()
print("Target numbers:", target_numbers)

while True:
    frame = capture_screen()
    focused_frame = crop_focus_area(frame)
    highlighted_frame = find_numbers(focused_frame, target_numbers)
    cv2.imshow('Number Finder', highlighted_frame)
    
    # Wait for a key press and handle events
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('p'):  # Example: Pause on 'p' key press
        cv2.waitKey(-1)  # Wait indefinitely until a key is pressed
    elif key == ord('r'):  # Example: Resume on 'r' key press
        continue  # Resume processing
    
    sleep(0.02)  # Adjust delay for smoother display updates

cv2.destroyAllWindows()
