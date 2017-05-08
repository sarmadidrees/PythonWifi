import I2Clcd_Lib
import time
import subprocess
import psutil
import os
from datetime import datetime
from datetime import timedelta
import RPi.GPIO as GPIO

wifiScriptPath = "/home/rospi/I2C_LCD/wifi_code.py" #to be added

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
    # need to change this and get SYSTEM UPTIME
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
	GPIO.remove_event_detect(4)
	global shuttingDown
	button_press_time = time.time()
	button_release_time = time.time()
	while GPIO.input(4)==False:
		time.sleep(1)
		button_release_time = time.time()
	print "PRESS TIME" + str(button_press_time)
	print "RELEASE TIME" + str(button_release_time)
	if button_release_time > (button_press_time+5):
		shuttingDown = 1
		mylcd.lcd_clear()
		mylcd.lcd_display_string_pos("SHUTTING DOWN...",1,0)
		print "SHUTTING DOWN"
		time.sleep(5)
		#subprocess.call(['sudo shutdown -h now'], shell = True)
	else:
		subprocess.call(['python '+ wifiScriptPath], shell = True)
		shuttingDown = 0
		GPIO.add_event_detect(4, GPIO.FALLING, callback=wifiCallback, bouncetime=200)

GPIO.add_event_detect(4, GPIO.FALLING, callback=wifiCallback, bouncetime=200)

#MAIN LOOP
screen = 1
while True:
	mylcd.lcd_clear()
	if (screen == 1 and shuttingDown==0):
		mylcd.lcd_display_string_pos(currentSSID(), 1,0)
		mylcd.lcd_display_string_pos(currentIP(), 2,0)
		#print currentSSID()
		#print currentIP()
		z = 0
		while (z<5 and shuttingDown==0):
			time.sleep(1)
			z = z+1
		screen = 2
		mylcd.lcd_clear()

	endTime = time.time() + 5
	time1 = currentTime()

	if (screen == 2 and shuttingDown==0):
		CPU_Temp_String = str(getCPUtemp()) + "C"
		CPU_Usage_String = str(getCPUuse()) + "%"
		mylcd.lcd_display_string_pos("UpTime:         ", 1,0)
		mylcd.lcd_display_string_pos("                ", 2,0)
		while (endTime > time.time() and shuttingDown==0):
			#if(currentTime() != time1):
				currentTime_String =  currentTime()
				mylcd.lcd_display_string_pos(currentTime_String, 1,7)
				mylcd.lcd_display_string_pos("                ", 2,0)
				mylcd.lcd_display_string_pos(CPU_Temp_String,2,0)
				mylcd.lcd_display_string_pos(CPU_Usage_String,2,9)
				#time1 = currentTime()
				time.sleep(1)
		screen = 1
