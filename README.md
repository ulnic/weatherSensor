# weatherSensor_rpi
Temperature, Weather and Light Reader for a Raspberry pi (any model)



#INSTALL SCRIPT DOES...
 TODO: Update description below and test


--ITEMS on Raspberry PI ZERO to be installed


sudo apt-get install python-pip
sudo apt-get install git
sudo apt-get install python-smbus
sudo apt-get install i2c-tools
sudo apt-get install python-dev 
sudo apt-get install python-rpi.gpio

ENABLE I2C:
sudo echo i2c-bcm2708 >> /etc/modules
sudo echo i2c-dev >> /etc/modules

sudo nano /boot/config.txt
and add/uncomment:
	dtparam=i2c1=on
	dtparam=i2c_arm=on


update rpi hostname

add cronjon
sudo crontab -e......