#weatherSensor
Temperature, Weather and Light Reader for a Raspberry pi (any model)



## INSTALL SCRIPT DOES...
 TODO: Update description below and test


--ITEMS on Raspberry PI ZERO to be installed



sudo apt-get --assume-yes install python-pip git python-smbus i2c-tools python-dev python-rpi.gpio


ENABLE I2C:
sudo echo i2c-bcm2708 >> /etc/modules
sudo echo i2c-dev >> /etc/modules

sudo nano /boot/config.txt
and add/uncomment:
	dtparam=i2c1=on
	dtparam=i2c_arm=on


pip install -r requirements.txt

update rpi hostname

add rc.local