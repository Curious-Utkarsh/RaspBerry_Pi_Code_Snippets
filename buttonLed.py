import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
buttonPin = 20
ledPin = 19
GPIO.setup(buttonPin, GPIO.IN)
GPIO.setup(ledPin, GPIO.OUT)
buttonVal = GPIO.input(buttonPin)
try:
	while(True):
		buttonVal = GPIO.input(buttonPin)
		if (buttonVal == 1):
			GPIO.output(ledPin, True)
		else:
			GPIO.output(ledPin, False)
except KeyboardInterrupt:
	GPIO.cleanup()

