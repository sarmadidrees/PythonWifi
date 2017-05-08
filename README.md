# PythonWifi
Simple Wifi terminal commands with python script using subprocess class

Launching a python script at Pi boot:
-edit rc.local with following command
 $ sudo nano /etc/rc.local
-Add commands to execute using absolute referencing of the file location (complete file path are preferred). Be sure to leave the line exit 0 at the end.
example: sudo python /home/pi/sample.py &
('&' make sures to not run in a forever loop)

-Current commands are
sudo python /home/rospi/I2C_LCD/wifi_code.py &
sudo python /home/rospi/I2C_LCD/LCD_code.py &

the /home/rospi/I2C_LCD/ is where we copied the script files.


DONE:
-Test on RspberryPi3
-Add I2C LCD
