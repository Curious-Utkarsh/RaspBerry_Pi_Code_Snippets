import cv2 
from picamera2 import Picamera2
from servo import Servo

print(cv2.__version__)

Width = 1280
Height = 720

piCam = Picamera2()
piCam.preview_configuration.main.size = (Width,Height)
piCam.preview_configuration.main.format = "RGB888"
piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()

pan = Servo(pin=13) #(BCM)
tilt = Servo(pin=12) 

panAngle = 0
tiltAngle = 50
flag = 0
faceDet = True
c = 0

pan.set_angle(panAngle)
tilt.set_angle(tiltAngle)

class mpFace:
    import mediapipe as mp
    def __init__(self):
        self.findFace=self.mp.solutions.face_detection.FaceDetection()
    def parseFaceBox(self,frame):
        frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=self.findFace.process(frameRGB)
        myFace=[]
        if results.detections != None:
            for face in results.detections:
                myFace=[]
                faceBox = face.location_data.relative_bounding_box
                topLeft = (int(faceBox.xmin*Width),int(faceBox.ymin*Height))
                w = int(faceBox.width*Width)
                h = int(faceBox.height*Height)
                cX = int((faceBox.xmin*Width) + w/2)
                cY = int((faceBox.ymin*Height) + h/2)
                centerP = (cX,cY)
                topRight = ((int(faceBox.xmin*Width)+w),(int(faceBox.ymin*Height)+h))
                myFace.append((topLeft,topRight,centerP))       
        return myFace

findFace=mpFace()

try :
    while True:
        frame=piCam.capture_array()
        frame = cv2.flip(frame, -1)
        myFaces=findFace.parseFaceBox(frame)
        if(myFaces == []):
            if(faceDet == True):
                c = c+1
            if(c == 50):
                faceDet = False
                c = 0
            if(faceDet == False):
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
            faceDet = True
            c = 0
        for face in myFaces:
            cv2.rectangle(frame,face[0],face[1],(0,100,255),3)
            cv2.circle(frame,face[2],15,(0,0,255),-1)
            errorPan = (face[2][0] - (Width/2))
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
                
            errorTilt = (face[2][1] - (Height/2))
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
