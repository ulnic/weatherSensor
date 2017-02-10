#weatherSensor
Temperature, Weather and Light Reader for a Raspberry pi (any model)

## Setup the Raspberry pi with

### Enable SSH & I2C
type 
```
sudo raspi-config
```
 Then select Advanced Options and enable SSH and I2C

alternative via:

ENABLE I2C:
sudo echo i2c-bcm2708 >> /etc/modules
sudo echo i2c-dev >> /etc/modules

sudo nano /boot/config.txt
and add/uncomment:
	dtparam=i2c1=on
	dtparam=i2c_arm=on

### Setup Network
* Setup wifi / ethernet to allow you to SSH into the raspberry pi

- _sudo nano /etc/wpa_supplicant/wpa_supplicant.conf_
- Add or edit 
```
network={
ssid="SSID"
psk="WIFI PASSWORD"
}
```

### Install git
_sudo apt-get install git_

## Install raspberry pi packages
_sudo apt-get --assume-yes install python-pip i2c-tools python-rpi.gpio_

--sudo apt-get --assume-yes install python-pip python-smbus i2c-tools python-dev python-rpi.gpio--


## Clone the weatherStation GIT Repository
_sudo git clone https://github.com/ulnic/weatherSensor.git_


# Configure weatherStation

1. pip install -r requirements.txt
2. Add rc.local
 Add below 2 lines just before the _exit 0_
 ``` 
# Execute weather sensor automatically at start up
sh /home/pi/weatherSensor/reboot_script_weatherSensor.sh 
```

https://github.com/eclipse/paho.mqtt.python


## Optional

# Update the raspberry pi hostname
_sudo raspi-config_ and here you can set the hostname of the raspberry pi

https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet