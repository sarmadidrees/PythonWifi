import I2Clcd_Lib
import time
import subprocess
from datetime import datetime
import RPi.GPIO as GPIO 

wifiScriptPath = "/home/"			#to be added

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(channel, GPIO.FALLING, callback=wifiCallback, bouncetime=200)

mylcd = I2Clcd_Lib.lcd()
mylcd.lcd_clear()

def currentSSID():
	SSID = subprocess.check_output(['iwgetid -r'], shell = True)
	return SSID

def currentIP():
	p = subprocess.Popen(['hostname', '-I'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	IP, err = p.communicate()
	return IP

def currentTime():
	string = str(datetime.now().strftime('%H:%M:%S %d/%m/%Y'))
	return string

def getCPUtemp():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

def getCPUuse():
    return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip(\)))

def wifiCallback(channel):
	subprocess.call(['python '+ wifiScriptPath], shell = True)



#MAIN LOOP
while True:
	if (screen == 1):
		mylcd.lcd_display_string_pos(currentSSID(), 1,0)
		mylcd.lcd_display_string_pos(currentIP(), 2,0)
		#print currentSSID()
		#print currentIP()
		time.sleep(5)
		screen = 2
		mylcd.lcd_clear()

	endTime = time.time() + 5
	time = currentTime()

	if (screen == 2):
		while (endTime > time.time()):
			if(currentTime() != time):
				mylcd.lcd_display_string_pos(currentTime(), 1,0)
				time = currentTime()
