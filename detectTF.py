import cv2
import time
from picamera2 import Picamera2

from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
import utils

model = 'efficientdet_lite0.tflite'
num_threads = 4

dispW = 1280
dispH = 720

piCam = Picamera2()
piCam.preview_configuration.main.size = (dispW,dispH)
piCam.preview_configuration.main.format = "RGB888"
piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()

# webcam = 'set yor webcam id (seeing lesson 63)'
# webCam = cv2.VideoCapture(webcam)
# webCam.set(cv2.CAP_PROP_FRAME_WIDTH, dispW)
# webCam.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)
# webCam.set(cv2.CAP_PROP_FPS, 30)

base_options = core.BaseOptions(file_name = model, use_coral = False, num_threads = num_threads)
detection_options = processor.DetectionOptions(max_results = 5, score_threshold = 0.3)
options = vision.ObjectDetectorOptions(base_options = base_options, detection_options = detection_options)
detector = vision.ObjectDetector.create_from_options(options)

while True:
    #ignore, frame = webCam.read()
    frame = piCam.capture_array()
    frame = cv2.flip(frame, -1)
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frameTensor = vision.TensorImage.create_from_array(frameRGB)
    detections = detector.detect(frameTensor)
    image = utils.visualize(frame, detections)
    
    cv2.imshow("piCamera 2", frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cv2.destroyAllWindows()