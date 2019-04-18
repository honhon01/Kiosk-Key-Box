import RPi.GPIO as GPIO
import time


#GPIO.setmode(GPIO.BCM)
#GPIO.setup(23, GPIO.OUT)
#GPIO.setup(24, GPIO.OUT)
#GPIO.setup(12, GPIO.OUT)
#GPIO.setup(16, GPIO.OUT)
	
def forward(tf):
	#init()
	print ("Unlocking")
	GPIO.output(23, True)
	GPIO.output(24, False)
	GPIO.output(12, True)
	GPIO.output(16, False)
	time.sleep(tf)
	print ("DONE")
	
	#GPIO.cleanup()
	
def reverse(tf):
	#init()
	print ("Locking")
	GPIO.output(23, False)
	GPIO.output(24, True)
	GPIO.output(12, False)
	GPIO.output(16, True)
	time.sleep(tf)
	print ("DONE")
	#GPIO.cleanup()
	
#print ("forward")
#forward(3)
#print ("reverse")
#reverse(3)
