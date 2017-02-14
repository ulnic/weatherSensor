# Raspberry Pi Weather Sensor

*Temperature, Weather and Light Reader for a Raspberry pi (any model)*

These instructions are for a simple Raspberry Pi project that can be used in any home automation, to collect temperature and humidity data. Just plug it in, configure the MQTT path and forget! 

## Needed parts:

* A [Raspberry Pi Zero](https://www.raspberrypi.org/products/pi-zero/).  Or any Raspberry Pi.
* Any old MicroSD card.  2GB is plenty.
* A USB WiFi dongle (and a MicroUSB adapter if you choose the Pi Zero)
* An [HTU21D-F Temperature & Humidity Sensor](https://learn.adafruit.com/adafruit-htu21d-f-temperature-humidity-sensor/overview)
* Any microUSB power source


# Step 1: Create the OS

> *Note*: We can skip plugging the Pi into a TV and keyboard by configuring the SD card directly from your computer. If you'd rather do this directly from the booted Pi, that works too!

1. [Download Raspbian Jessie Lite](https://www.raspberrypi.org/downloads/raspbian/) and image it onto an SD card 

2. Mount the SD card on your computer.  There should be two partitions, a FAT32 **boot partition**, and an EXT3 **OS partition**.  On [Mac](https://osxfuse.github.io/) or [Windows](http://www.chrysocome.net/explore2fs), you may need to find a driver to see EXT3 partitions (see links).

3. Add an empty file named `ssh` to the **boot partition**.  This enables the ssh daemon.

4. Edit these files on the **OS partition**:
  * Edit `/etc/hostname` and `/etc/hosts` to change “raspberrypi” to a **unique host name**
  * Edit `/etc/wpa_supplicant/wpa_supplicant.conf` to add your WiFi authentication:

```
    network={
	    ssid="your WiFi name (SSID)"
	    psk="your WiFi password"
    }
```

Your OS should now be ready to boot and automatically jump on your home network!



# Step 2: Create the hardware

1. Insert the microSD card into the Raspberry Pi.

2. Add the WiFi dongle to Raspberry Pi USB port.  A Raspberry Pi Zero will need a [microUSB adaptor](https://www.amazon.com/gp/product/B015GZOHKW/).

3. Add the HTU21D-F Temperature & Humidity Sensor to [Raspberry Pi GPIO pins](https://pinout.xyz/). 

4. Plug in a power source, and you’re good to go.  Within a few seconds, you should be able to connect to the Pi with: “ssh pi@*{**unique host name**}*” (password: `raspberry`)



# Step 3: Create the software

After you ssh to the pi, install a few essential libraries:

    sudo apt-get --assume-yes install python-pip i2c-tools git
    
Set the timezone to make sure timestamps are correct

    sudo raspi-config
    [Internationalisation Options]
    [Change Timezone]

Clone the weatherSensor github repository

    sudo git clone https://github.com/ulnic/weatherSensor.git
    
Install weatherSensor dependencies (this includes [RPI.GPIO](https://pypi.python.org/pypi/RPi.GPIO) and [MQTT PAHO](https://eclipse.org/paho/))

    pip install -r requirements.txt



Create the settings file `/home/pi/weatherSensor/config/configuration.ini`.  This file specifies what sensor pin to monitor, what messages you want, and what services to send the message to. 

* If you want PushBullet notifications, create a PushBullet Access Token key here:  https://www.pushbullet.com/#settings/account
* If you want Twitter notifications, create Twitter API keys here (Steps 1-4): http://nodotcom.org/python-twitter-tutorial.html

Edit `/etc/rc.local` to make the program run when the device boots up.

Add before the `exit` line:

    # Execute weather sensor automatically at start up
    sh /home/pi/weatherSensor/reboot_script_weatherSensor.sh 

You’re done!  Reboot and test it out.




# Delete below
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



### Install raspberry pi packages
_sudo apt-get --assume-yes install python-pip i2c-tools python-rpi.gpio_

--sudo apt-get --assume-yes install python-smbus python-dev python-rpi.gpio--


### Configure weatherStation


https://github.com/eclipse/paho.mqtt.python


https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet