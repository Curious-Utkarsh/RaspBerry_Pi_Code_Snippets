from ultralytics import YOLO
import cv2
import pyttsx3
import time

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Set speech speed

# Load YOLOv8 pretrained model
model = YOLO("yolov8n.pt")

# Open webcam
cap = cv2.VideoCapture(0)

# Buffer to keep track of last spoken objects
spoken_objects = {}
speak_interval = 5  # seconds before repeating the same object

def speak(text):
    engine.say(text)
    engine.runAndWait()

print("[INFO] Starting webcam. Press 'q' to quit...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run detection
    results = model(frame)[0]

    # Get current time
    current_time = time.time()

    # Extract detected object names
    detected = set()
    for box in results.boxes:
        cls_id = int(box.cls[0])
        label = model.names[cls_id]
        detected.add(label)

    # Speak detected objects (avoid repeats within speak_interval)
    for obj in detected:
        last_spoken = spoken_objects.get(obj, 0)
        if current_time - last_spoken > speak_interval:
            speak(f"I see a {obj}")
            spoken_objects[obj] = current_time

    # Show annotated frame
    annotated_frame = results.plot()
    cv2.imshow("YOLOv8 Detection", annotated_frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
