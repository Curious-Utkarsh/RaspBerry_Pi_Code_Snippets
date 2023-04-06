import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
servoPin = 17
button1 = 20
button2 = 5
pwmVal = 0
GPIO.setup(servoPin, GPIO.OUT)
GPIO.setup(button1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(button2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
pwm = GPIO.PWM(servoPin, 50)
pwm.start(0)

try :
    while True:
        buttonVal1 = GPIO.input(button1)
        buttonVal2 = GPIO.input(button2) #input(in degrees)/12
        if (buttonVal1 == 0):
            pwmVal = pwmVal + 1
        if (buttonVal2 == 0):
            pwmVal = pwmVal - 1
        if (pwmVal > 15):
            pwmVal = 15
        if (pwmVal < 0):
            pwmVal = 0
        pwm.ChangeDutyCycle(pwmVal)
        sleep(0.08)

except KeyboardInterrupt :
    pwm.stop()
    GPIO.cleanup()
    print("Clean Up Done")