import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
pwmPin = 17

GPIO.setup(pwmPin, GPIO.OUT)
pwm = GPIO.PWM(pwmPin, 50) #While using servo motor always keep freq. as 50
pwm.start(0)

#Note : For Small Blue Servo which i have, 0 degree is pwm 1 and 180 degree is pwm 15.
#       it maybe different for different servos.
# On applying PWM as 0 servo motor will stop vibrating.

try :
    while True:
        pwmPercent = float(input("PWM % "))
        pwm.ChangeDutyCycle(pwmPercent)
        sleep(0.1)
                           
except KeyboardInterrupt :
    GPIO.cleanup()
    print("Cleanup Done")