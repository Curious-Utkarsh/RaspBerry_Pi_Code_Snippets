import cv2
import pytesseract
import pyttsx3
import time

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Open webcam
cap = cv2.VideoCapture(0)

# Variables to avoid repeating speech
last_read_text = ""
read_interval = 5  # seconds between speaking same thing
last_read_time = time.time()

# Tesseract OCR config: OCR Engine Mode and Page Segmentation Mode
custom_config = r'--oem 3 --psm 6'

def speak(text):
    engine.say(text)
    engine.runAndWait()

print("[INFO] Starting OCR Reader. Press 'q' to quit...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize for better OCR performance
    frame = cv2.resize(frame, None, fx=1.5, fy=1.5)

    # Preprocessing
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # OCR on the processed frame
    text = pytesseract.image_to_string(thresh, config=custom_config).strip()

    # Current timestamp
    current_time = time.time()

    # Speak only if:
    # - text exists
    # - it has at least 2 words (to avoid junk)
    # - it's new or enough time has passed
    if text and len(text.split()) >= 2 and text != last_read_text and (current_time - last_read_time) > read_interval:
        print(f"[OCR] {text}")
        speak(text)
        last_read_text = text
        last_read_time = current_time

    # Show the processed camera feed
    cv2.imshow("OCR Webcam Reader", thresh)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
