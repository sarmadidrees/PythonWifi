
import time
import subprocess

#subprocess.call(['ifconfig wlp7s0 down'], shell = True)
#time.sleep(1)
#subprocess.call(['ifconfig wlp7s0 up'], shell = True)
#time.sleep(1)

wifiList = []
priorityList = [
				['ZONG-MBB-B310-02F1','1J3E47HQR381'],
				['IMRLab','1qazxsw23edc'],
				['Tajurbagah','96020029'],
				['maaz1','786786786']
				]


def scanWifi():
	l1,l2 = 0,0
	global wifiList
	
	totalList = subprocess.check_output(['iwlist wlan0 s'], shell = True)
	complete = totalList.find('Cell')

	while (complete != -1):
		l1 = totalList.find('ESSID:"',l2)
		l2 = totalList.find('"',l1+7)
		wifiList.append(totalList[l1+7:l2])
		complete = totalList.find('Cell',l2) 


def connectWifi():
	x = 0
	lenght = len(priorityList)
	connected = False

	for nameP,password in priorityList:
		for nameC in wifiList:
			if nameP == nameC:
				#subprocess.call(['nmcli con modify '+str(priorityList[x][0])+' wifi-sec.key-mgmt wpa-psk'], shell = True )
				#time.sleep(2)
				#subprocess.call(['nmcli con modify '+priorityList[x][0]+' wifi-sec.psk '+priorityList[x][1]], shell = True)	
				#time.sleep(2)
				subprocess.call(['nmcli d wifi connect '+priorityList[x][0]+' password '+priorityList[x][1]], shell = True)
				connected = True
				break

		x = x+1
		if x==lenght or connected==True:
			break


'''
#for just checking/print in console
def currentSSID():
	SSID = subprocess.check_output(['iwgetid -r'], shell = True)
	return SSID

def currentIP():
	p = subprocess.Popen(['hostname', '-I'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	IP, err = p.communicate()
	return IP
'''

scanWifi()	
connectWifi()