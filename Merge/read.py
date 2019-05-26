import RPi.GPIO as GPIO
import SimpleMFRC522

reader = SimpleMFRC522.SimpleMFRC522()

def RFIDread():
    while 1:
        id,text = reader.read()
        text = text.replace(' ','')
        if text == 'CPE1121':
            break
        else:
            print('Invalid RFID')
	
