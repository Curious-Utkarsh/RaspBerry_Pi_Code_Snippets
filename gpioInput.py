 import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.IN)
try:
	while True:
		inVal = GPIO.input(20)
		print(inVal)
		sleep(.1)
except KeyboardInterrupt:
	GPIO.cleanup()
