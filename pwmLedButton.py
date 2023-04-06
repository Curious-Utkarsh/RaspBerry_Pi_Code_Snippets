import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
led = 13
dimSwitch = 12
briSwitch = 20
preValDim = 1
curValDim = 1
preValBri = 1
curValBri = 1
cnt = 10
GPIO.setup(led, GPIO.OUT)
GPIO.setup(dimSwitch, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(briSwitch, GPIO.IN, pull_up_down = GPIO.PUD_UP)
myPWM = GPIO.PWM(led, 100)
myPWM.start(0)
try :
	while True:
		curValDim = GPIO.input(dimSwitch)
		curValBri = GPIO.input(briSwitch)
		if((curValBri - preValBri) == -1):
			print("BRIGHT")		
			cnt = cnt+10
		if((curValDim - preValDim) == -1):
			print("DIM")
			cnt = cnt-10
		if(cnt < 0):
			cnt = 0
		if(cnt > 100):
			cnt = 100
		myPWM.ChangeDutyCycle(cnt)
		preValBri = curValBri 
		preValDim = curValDim
except KeyboardInterrupt:
	myPWM.stop()
	GPIO.cleanup()
