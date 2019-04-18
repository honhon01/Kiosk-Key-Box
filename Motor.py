import RPi.GPIO as gpio
import time

def init():
	gpio.setmode(gpio.BCM)
	gpio.setup(23, gpio.OUT)
	gpio.setup(24, gpio.OUT)
	gpio.setup(12, gpio.OUT)
	gpio.setup(16, gpio.OUT)
	
def forward(tf):
	init()
	gpio.output(23, True)
	gpio.output(24, False)
	gpio.output(12, True)
	gpio.output(16, False)
	time.sleep(tf)
	gpio.cleanup()
	
def reverse(tf):
	init()
	gpio.output(23, False)
	gpio.output(24, True)
	gpio.output(12, False)
	gpio.output(16, True)
	time.sleep(tf)
	gpio.cleanup()
	
print ("forward")
forward(3)
print ("reverse")
reverse(3)
