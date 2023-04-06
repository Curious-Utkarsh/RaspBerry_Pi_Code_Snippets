import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
ledPin = 19
buttonPin = 20
ledState = 0
curVal = 1
preVal = 1
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
try :
	while True:
		curVal = GPIO.input(buttonPin)
		print(curVal)
		if((preVal - curVal) == 1):
			if(ledState == 0):
				GPIO.output(ledPin, True)
				ledState = 1
			else:
				GPIO.output(ledPin, False)
				ledState = 0
		preVal = curVal

except KeyboardInterrupt :
	GPIO.cleanup()
