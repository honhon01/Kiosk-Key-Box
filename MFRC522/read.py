#!/usr/bin/env python
import RPi.GPIO as GPIO
import SimpleMFRC522

reader = SimpleMFRC522.SimpleMFRC522()

try:
	id,text = reader.read()
	text = text.replace(' ','')
	if text == 'CPE1126':
		print('sure')
	else:
		print('no')
	print(text)
finally:
	GPIO.cleanup()
