import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
led = 19
GPIO.setup(led, GPIO.OUT)
myPWM = GPIO.PWM(led, 100) #100 is PWM Frequency...keep it 100 only..100cycles/sec
myPWM.start(0) #50 is PWM dutyCycle you can change that
for i in range(1, 100, 1):
	myPWM.ChangeDutyCycle(i)
	sleep(0.1)
myPWM.stop()
GPIO.cleanup()
