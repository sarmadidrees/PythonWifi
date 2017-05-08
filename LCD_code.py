import I2Clcd_Lib
import time
import subprocess
import psutil
import os
from datetime import datetime
import RPi.GPIO as GPIO

_debug_ = False 		#for debug 
btn_pressed = False
 
wifiScriptPath = "/home/rospi/I2C_LCD/wifi_code.py" #wifi code path

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

mylcd = I2Clcd_Lib.lcd()
mylcd.lcd_clear()

shuttingDown=0
 
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
	# string = str(datetime.now().strftime('%H:%M:%S'))
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
	time_string = str(int(uptime_seconds/3600)) + ':' + str(int(uptime_seconds/60)) + ':' + str(int(uptime_seconds)%60)
	return time_string

def getCPUtemp():
	res = os.popen('vcgencmd measure_temp').readline()
    	return(res.replace("temp=","").replace("'C\n",""))

def getCPUuse():
  	return psutil.cpu_percent()

def wifiCallback(channel):
	global btn_pressed
	time.sleep(.2)
	if (GPIO.input(4)==False):
		btn_pressed = True
		print "callback"

GPIO.add_event_detect(4, GPIO.FALLING, callback=wifiCallback, bouncetime=600)

#MAIN LOOP
screen = 1
while True:
	mylcd.lcd_clear()
	if (screen == 1):
		if _debug_:
			print currentSSID()
			print currentIP()
		else:
			mylcd.lcd_clear()
			mylcd.lcd_display_string_pos(currentSSID(), 1,0)
			mylcd.lcd_display_string_pos(currentIP(), 2,0)

		z = 0
		while (z<5 and btn_pressed == False):
			time.sleep(1)
			z = z+1
		screen = 2
		mylcd.lcd_clear()

	endTime = time.time() + 5
	time1 = currentTime()

	if (screen == 2):
		CPU_Temp_String = str(getCPUtemp()) + "C"
		CPU_Usage_String = str(getCPUuse()) + "%"
		mylcd.lcd_display_string_pos("Uptime:          ", 1,0)			#uncomment later
		#mylcd.lcd_display_string_pos("                ", 2,0)
		while (endTime > time.time() and btn_pressed == False):
			if(currentTime() != time1):
				currentTime_String =  currentTime()
				if _debug_:
					print currentTime_String
				else:
					mylcd.lcd_display_string_pos(currentTime_String, 1,7)
					#mylcd.lcd_display_string_pos("                ", 2,0)
					mylcd.lcd_display_string_pos(CPU_Temp_String,2,0)
					mylcd.lcd_display_string_pos(CPU_Usage_String,2,9)
					time1 = currentTime()
		screen = 1

	if (btn_pressed == True):
		print "IN"
		btn_press_time = time.time()
		btn_release_time = time.time()
		while GPIO.input(4)==False:
			time.sleep(1)
			btn_release_time = time.time()
		print str(btn_press_time)
		print str(btn_release_time)
		if btn_release_time > (btn_press_time+5):
			if (_debug_):
				print "Shutdown"
			else:
				mylcd.lcd_clear()
				mylcd.lcd_display_string_pos("Shutting Down....",1,0)
				time.sleep(5)
				subprocess.call(['shutdown -P now'], shell = True)
		else:
			if (_debug_):
				print "Wifi script"
				subprocess.call(['python '+ wifiScriptPath], shell = True)
				time.sleep(2)
			else:
				mylcd.lcd_clear()
				mylcd.lcd_display_string_pos("Launching Wifi",1,0)
				mylcd.lcd_display_string_pos("Python Script",2,0)
				subprocess.call(['python '+ wifiScriptPath], shell = True)
				time.sleep(2)
		btn_pressed = False
		#screen = 1
