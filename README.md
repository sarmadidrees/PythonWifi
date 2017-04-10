# PythonWifi
Simple Wifi terminal commands with python script using subprocess class

Launching a python script at Pi boot:
-edit rc.local with following command
 $ sudo nano /etc/rc.local
-Add commands to execute using absolute referencing of the file location (complete file path are preferred). Be sure to leave the line exit 0 at the end.
example: sudo python /home/pi/sample.py &


TODO:
-Test on RspberryPi3
-Add I2C LCD
