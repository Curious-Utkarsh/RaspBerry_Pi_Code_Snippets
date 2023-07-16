import cv2 
from picamera2 import Picamera2
import mediapipe as mp
from servo import Servo

print(cv2.__version__)

width = 1280
height = 720

piCam = Picamera2()
piCam.preview_configuration.main.size = (width,height)
piCam.preview_configuration.main.format = "RGB888"
piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()

handsDetect=mp.solutions.hands.Hands(1,1,False,.5,.5)
mpDraw=mp.solutions.drawing_utils

pan = Servo(pin=13) # pan_servo_pin (BCM)
tilt = Servo(pin=12) 

panAngle = 0
tiltAngle = 50
flag = 0
handDet = True
c = 0

pan.set_angle(panAngle)
tilt.set_angle(tiltAngle)

def parseLandMarks(frame):
    myHands=[]
    frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results=handsDetect.process(frameRGB)
    if results.multi_hand_landmarks != None:
        for handLandMarks in results.multi_hand_landmarks:
            myHand=[]
            for LandMark in handLandMarks.landmark:
                myHand.append((int(LandMark.x*width),int(LandMark.y*height)))
            myHands.append(myHand)
    return myHands

try :
    while True:
        frame=piCam.capture_array()
        frame = cv2.flip(frame, -1)
        MYHands=parseLandMarks(frame)
        if(MYHands == []):
            if(handDet == True):
                c = c+1
            if(c == 50):
                handDet = False
                c = 0
            if(handDet == False):
                if(flag == 0):
                    panAngle = panAngle + 2
                    if(panAngle > 90):
                        flag = 1
                        panAngle = 90
                        tiltAngle = tiltAngle - 10
                if(flag == 1):
                    panAngle = panAngle - 2
                    if(panAngle < -90):
                        panAngle = -90
                        flag = 0
                        tiltAngle = tiltAngle - 10
                if(tiltAngle <= 20):
                    tiltAngle = 70
                pan.set_angle(panAngle)
                tilt.set_angle(tiltAngle)
        else:
            handDet = True
            c = 0
        for oneHand in MYHands:
            cv2.circle(frame,oneHand[8],15,(0,0,255),-1)
            errorPan = (oneHand[8][0] - (width/2))
            if(errorPan > 30):
                #panAngle = panAngle - 2
                panAngle = panAngle - (errorPan/70) #every time we want to pan proportinal to error/2 and 1 degree is 35 pixel so error angle in terms of error is ((error/(35))/2) 
                if(panAngle < -90):
                    panAngle = -90
                pan.set_angle(panAngle)
            if(errorPan < -30):
                #panAngle = panAngle + 2
                panAngle = panAngle - (errorPan/70)
                if(panAngle > 90):
                    panAngle = 90
                pan.set_angle(panAngle)
                
            errorTilt = (oneHand[8][1] - (height/2))
            if(errorTilt > 30):
                #tiltAngle = tiltAngle + 2
                tiltAngle = tiltAngle + (errorTilt/70)
                if(tiltAngle > 90):
                    tiltAngle = 90
                tilt.set_angle(tiltAngle)
            if(errorTilt < -30):
                #tiltAngle = tiltAngle - 2
                tiltAngle = tiltAngle + (errorTilt/70)
                if(tiltAngle < -90):
                    tiltAngle = -90
                tilt.set_angle(tiltAngle)        
        cv2.imshow('my WEBcam',frame)
        cv2.moveWindow('my WEBcam',50,0)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break
    cv2.destroyAllWindows()
    
except KeyboardInterrupt :
    GPIO.cleanup()