import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
trigPin = 23
echoPin = 24
GPIO.setup(trigPin, GPIO.OUT)
GPIO.setup(echoPin, GPIO.IN)

try :
    while True:
        GPIO.output(trigPin, 0)
        time.sleep(2E-6) #2 microseconds
        GPIO.output(trigPin, 1)
        time.sleep(10E-6) #10 microseconds
        GPIO.output(trigPin, 0)
        while (GPIO.input(echoPin) == 0) :
            pass
        echoStartTime = time.time() #millis()
        while (GPIO.input(echoPin) == 1):
            pass
        echoStopTime = time.time()
        pingTravelTime = echoStopTime - echoStartTime
        #print(int(pingTravelTime*1E6)) #1E6 represents microseconds
        distTravel = int(pingTravelTime*17143.984)
        print(distTravel, "cm")
        time.sleep(0.2)
        
except KeyboardInterrupt :
    GPIO.cleanup()
    print("Cleanup Done")
