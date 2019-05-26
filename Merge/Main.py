import RPi.GPIO as GPIO
import time
import Motor
import read
import datetime
import http.client
import json

from pad4pi import rpi_gpio

#******************************************#
KEYPAD = [
    ["1", "2", "3"],
    ["4", "5", "6"],
    ["7", "8", "9"],
    ["*", "0", "#"]
]

COL_PINS = [17,27,22] # BCM numbering
ROW_PINS = [14,5,18,4] # BCM numbering

factory = rpi_gpio.KeypadFactory()
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

passW = ""
counter = 0
def printKey(key):
    global passW
    global counter
    passW = passW + key
    if key == "*":
        passW = ""
        lcd_string("   Insert PIN",LCD_LINE_2)
    else:
        lcd_string(passW,LCD_LINE_2)
    if len(passW) == 6:
		################ send pin to check with API ###############
        conn = http.client.HTTPSConnection("carto.cpe.kmutt.ac.th")
        conn.request("GET", "/pin/validate?Pin="+passW)
        r1 = conn.getresponse()
        dataGet = r1.read().decode('utf-8')
        conn.close()
        print("------- Check With API-------")
        print("Status   = " + str(r1.status), r1.reason)
        print("Response = " + dataGet)
        jsonData = json.loads(dataGet)
        if jsonData["open"] == True:
            jsonstr = str(jsonData["data"])
            tempStr = jsonstr.split('UsageID\':')
            tempStr = tempStr[1].split(',')
            UsageID = tempStr[0]
            print("***Correct PIN***")
            print("-----------------------------")
            lcd_string("    Correct!",LCD_LINE_2)
            passW = ""
            lcd_string(" Checking RFID!",LCD_LINE_2)
            read.RFIDread()
            print("RFID Valid! Opening the door")
            lcd_string("Unlocking!",LCD_LINE_2)
            Motor.reverse(5) #Motor open door
            #Motor.stop(1) #Stop the Motor
            lcd_string("Pick up the Key!",LCD_LINE_2)
            PickupTime = datetime.datetime.now()
            print("--------- Key Usage ---------")
            print("Key Pick Up Time   = " + str(PickupTime))
            while 1:
                starttime = time.time()
                read.RFIDread()
                endtime = time.time()
                time.sleep(1)
                if endtime-starttime > 5:
                    KeyUseTime = endtime-starttime
                    ReturnTime = datetime.datetime.now()
                    print("Key Return Time    = " + str(ReturnTime))
                    print("Total Key Use Time = " + str(KeyUseTime))
                    print("-----------------------------")
                    break
            lcd_string("  Key Returned",LCD_LINE_2)
            time.sleep(2)
            lcd_string("Locking The Door",LCD_LINE_2)
            Motor.forward(5) #Motor Close Door
            #Motor.stop(1) #Stop the Motor
            lcd_string("  Door Locked!",LCD_LINE_2)
            time.sleep(2)
            lcd_string("   Completed!",LCD_LINE_1)
            lcd_string("     Enjoy!",LCD_LINE_2)
            ################ send RoomUse information back to API ###############
            if KeyUseTime < 180:
                ReInTime = 'true'
            else:
                ReInTime = 'false'
            BODY = "{\"UsageID\":"+UsageID+",\"ReturnInTime\":"+ReInTime+ "}"
            headers = {"Content-Type":"application/json","Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IjU4MDcwNTAzNDM4IiwiaWF0IjoxNTU1MDUzMTEwfQ.vFrdCwfSSQQ3UXpPruawuUOze0FCu_lbOHnFP2KcQqY"}
            conn = http.client.HTTPSConnection("carto.cpe.kmutt.ac.th")
            conn.request("PUT", "/pin/status", BODY,headers)
            r1 = conn.getresponse()
            dataPut = r1.read().decode('utf-8')
            conn.close()
            print("----- Send Result to API -----")
            print("Status    = " + str(r1.status), r1.reason)
            print("Data send = " + BODY)
            print("Response  = " + dataPut)
            print("------------------------------")
            ################ close API ###############
            time.sleep(5)
            GPIO.output(LCD_ON, False)
            print('LCD off! Wait for trigger from API')
            time.sleep(5)
            GPIO.output(LCD_ON, True)
            print('LCD on!  Ready to recieve new PIN')
            lcd_string("    Welcome!",LCD_LINE_1)
            lcd_string("   Insert PIN",LCD_LINE_2)
        else:
            print("***Invalid PIN***")
            print("-----------------------------")
            lcd_string("  Invalid PIN!",LCD_LINE_2)
            time.sleep(2)
            lcd_string("   Insert PIN",LCD_LINE_2)
            counter += 1
            if counter == 3:
                print("Keybox Disabled for 20 Seconds")
                lcd_string("Keybox Disabled",LCD_LINE_1) #Keybox is Disabled
                lcd_string(" for 20 seconds",LCD_LINE_2) #try again in 20 seconds
                time.sleep(20)
                counter = 0
                print("Please Insert PIN again!")
                lcd_string("    Welcome!",LCD_LINE_1)
                lcd_string("   Insert PIN",LCD_LINE_2)
            passW = ""

#******************************************#

# printKey will be called each time a keypad button is pressed

keypad.registerKeyPressHandler(printKey)



# Define GPIO to LCD mapping
LCD_RS = 21
LCD_E  = 20
LCD_D4 = 26
LCD_D5 = 19
LCD_D6 = 13
LCD_D7 = 6
LCD_ON = 15


# Define LCD parameters
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005


#******************************************#
def main():
  # Main program block
  global pm
  global system_sts
  global passW
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
  GPIO.setup(LCD_E, GPIO.OUT)  # E
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7
  GPIO.setup(23, GPIO.OUT) #Motor1
  GPIO.setup(24, GPIO.OUT) #Motor2
  GPIO.setup(12, GPIO.OUT) #Motor3
  GPIO.setup(16, GPIO.OUT) #Motor4
  GPIO.setup(LCD_ON,GPIO.OUT)
  
  #Stop Motor
  GPIO.output(23, False)
  GPIO.output(24, False)
  GPIO.output(12, False)
  GPIO.output(16, False)
  
  # Initialise display
  lcd_init()
  lcd_byte(0x01, LCD_CMD)
  lcd_string("    Welcome!",LCD_LINE_1)
  lcd_string("   Insert PIN",LCD_LINE_2)
  lcd_byte(0xC0, LCD_CMD)
  GPIO.output(LCD_ON, True)
  while True:
      time.sleep(1)
      #if passW == "":
      #  lcd_string("",LCD_LINE_2)

      
#******************************************#  
def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)
  
#******************************************#
def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command

  GPIO.output(LCD_RS, mode) # RS

  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  lcd_toggle_enable()

  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  lcd_toggle_enable()
  
#******************************************#
def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)
  
#***************************************#


def lcd_string(message,line):
  # Send string to display
  
      
  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)
  
  

#******************************************#






    

if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)
    lcd_string("Goodbye!",LCD_LINE_1)
    GPIO.cleanup()

