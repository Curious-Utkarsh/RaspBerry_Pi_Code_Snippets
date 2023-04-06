import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
redLed = 19
greenLed = 13
ON = 1
OFF = 0
check = "y"
GPIO.setup(redLed, GPIO.OUT)
GPIO.setup(greenLed, GPIO.OUT)
while(check == "y"):
	led = input("Enter LED to Blink : ")
	cnt = int(input("ENTER LED Blinking Count : "))
	if(led == "Red"):
		for i in range(0, cnt, 1):
			GPIO.output(redLed, ON)
			time.sleep(1)
			GPIO.output(redLed, OFF)
			time.sleep(1)
	if(led == "Green"):
		for i in range(0, cnt, 1):
			GPIO.output(greenLed, ON)
			time.sleep(1)
			GPIO.output(greenLed, OFF)
			time.sleep(1)
	check = input("Run once more?? : ")
GPIO.cleanup()
