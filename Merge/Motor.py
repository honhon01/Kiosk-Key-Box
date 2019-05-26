import RPi.GPIO as GPIO
import time

	
def forward(tf):
	print ("Locking")
	GPIO.output(23, True)
	GPIO.output(24, False)
	GPIO.output(12, True)
	GPIO.output(16, False)
	time.sleep(tf)
	print ("Locked")
	
	
def reverse(tf):
	print ("Unlocking")
	GPIO.output(23, False)
	GPIO.output(24, True)
	GPIO.output(12, False)
	GPIO.output(16, True)
	time.sleep(tf)
	print ("Unlocked")
	
def stop(tf):
	GPIO.output(23, False)
	GPIO.output(24, False)
	GPIO.output(12, False)
	GPIO.output(16, False)
	time.sleep(tf)
