import I2Clcd_Lib
import time
from datetime import datetime

mylcd = I2Clcd_Lib.lcd()
mylcd.lcd_clear()

def currentSSID():
	SSID = subprocess.check_output(['iwgetid -r'], shell = True)
	return SSID

def currentIP():
	p = subprocess.Popen(['hostname', '-I'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	IP, err = p.communicate()
	return IP



mylcd.lcd_display_string_pos(currentSSID(), 1,0)
mylcd.lcd_display_string_pos(currentIP(), 2,0)

