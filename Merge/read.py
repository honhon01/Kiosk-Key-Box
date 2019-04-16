#!/usr/bin/env python
import RPi.GPIO as GPIO
import SimpleMFRC522

reader = SimpleMFRC522.SimpleMFRC522()

def RFIDread():
	print('Place RFID to read...')
	id,text = reader.read()
	text = text.replace(' ','')
	if text == 'CPE1121':
		print('Correct Data = ' + text)
	else:
		print('Wrong   Data = ' + text)
	
	#GPIO.cleanup()


#RFIDread()
