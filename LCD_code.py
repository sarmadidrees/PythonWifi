import I2Clcd_Lib
import time
import subprocess
import psutil
import os
from datetime import datetime
import RPi.GPIO as GPIO 

wifiScriptPath = "/home/rospi/I2C_LCD/wifi_code.py"		#to be added

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

mylcd = I2Clcd_Lib.lcd()
mylcd.lcd_clear()

def currentSSID():
	status = subprocess.check_output(['iw wlan0 link'], shell = True)
	SSID = "Not Connected"
	if (status.startswith('Not connected') == False):
		SSID = subprocess.check_output(['iwgetid -r'], shell = True)
	
	return SSID

def currentIP():
	p = subprocess.Popen(['hostname', '-I'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	IP, err = p.communicate()
	return IP

def currentTime():
	string = str(datetime.now().strftime('%H:%M:%S'))
	return string

def getCPUtemp():
	res = os.popen('vcgencmd measure_temp').readline()
    	return(res.replace("temp=","").replace("'C\n",""))

def getCPUuse():
  	return psutil.cpu_percent()

def wifiCallback(channel):
	subprocess.call(['python '+ wifiScriptPath], shell = True)


GPIO.add_event_detect(4, GPIO.FALLING, callback=wifiCallback, bouncetime=200)

#MAIN LOOP
screen = 1
while True:
	mylcd.lcd_clear()
	if (screen == 1):
		mylcd.lcd_display_string_pos(currentSSID(), 1,0)
		mylcd.lcd_display_string_pos(currentIP(), 2,0)
		#print currentSSID()
		#print currentIP()
		time.sleep(5)
		screen = 2
		mylcd.lcd_clear()

	endTime = time.time() + 5
	time1 = currentTime()

	if (screen == 2):
		CPU_Temp_String = str(getCPUtemp()) + "C"
		CPU_Usage_String = str(getCPUuse()) + "%"
		while (endTime > time.time()):
			if(currentTime() != time1):
				currentTime_String = "Time: " + currentTime()
				mylcd.lcd_clear()
				mylcd.lcd_display_string_pos(currentTime_String, 1,0)
				mylcd.lcd_display_string_pos(CPU_Temp_String,2,0)
				mylcd.lcd_display_string_pos(CPU_Usage_String,2,9)
				time1 = currentTime()
		screen = 1

