import cv2
from picamera2 import Picamera2
import mediapipe as mp

print(cv2.__version__)

width = 1280
height = 720

cam=Picamera2()
cam.preview_configuration.main.size = (1280,720)
cam.preview_configuration.main.format="RGB888"
cam.preview_configuration.align()
cam.configure("preview")
cam.start()

poseDetect=mp.solutions.pose.Pose(False,1,True,False,True,.5,.5)
#poseDetect=mp.solutions.pose.Pose("Is it static Image"-FALSE,"Do you want Pose of only Upper Body"-if yes-TRUE, if want full body-FALSE,"smoothData"-TRUE,.5,.5)
mpDraw=mp.solutions.drawing_utils

while True:
    frame=cam.capture_array()
    frame=cv2.flip(frame,1)
    frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results=poseDetect.process(frameRGB)
    if results.pose_landmarks != None:
        mpDraw.draw_landmarks(frame,results.pose_landmarks,mp.solutions.pose.POSE_CONNECTIONS)
        myBody=[]
        for LandMark in results.pose_landmarks.landmark:
            myBody.append((int(LandMark.x*width),int(LandMark.y*height)))
    cv2.imshow('my Cam',frame)   
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cv2.destroyAllWindows()