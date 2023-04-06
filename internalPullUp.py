import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
ledPin = 19
buttonPin = 20
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN,pull_up_down = GPIO.PUD_UP)
try :
	while True:
		buttonVal = GPIO.input(buttonPin)
		#print(str(buttonVal)+'\n')
		if (buttonVal == 0):
			GPIO.output(ledPin, True)
		else:
			GPIO.output(ledPin, False)
except KeyboardInterrupt :
	GPIO.cleanup() 
