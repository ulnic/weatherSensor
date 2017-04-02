# Raspberry Pi Weather Sensor

*Temperature, Weather and Light Reader for a Raspberry pi (any model)*

These instructions are for a simple Raspberry Pi project that can be used in any home automation, to collect temperature and humidity data. Just plug it in, configure the MQTT path and forget! 

## Needed parts:

* A [Raspberry Pi Zero](https://www.raspberrypi.org/products/pi-zero/).  Or any Raspberry Pi.
* Any MicroSD card. 
* A USB WiFi dongle (and a OTG adapter if you choose the Pi Zero)
* An [HTU21D-F Temperature & Humidity Sensor](https://learn.adafruit.com/adafruit-htu21d-f-temperature-humidity-sensor/overview)
* Any microUSB power source


# Step 1: Create the OS

> *Note*: We can skip plugging the Pi into a TV and keyboard by configuring the SD card directly from your computer. If you'd rather do this directly from the booted Pi, that works too!

1. [Download Raspbian Jessie Lite](https://www.raspberrypi.org/downloads/raspbian/) and image it onto an SD card 

2. Mount the SD card on your computer. Easiest is to follow the [RPi guide](https://www.raspberrypi.org/documentation/installation/installing-images/README.md)

3. Add an empty file named `ssh` to the **boot partition**.  This enables the ssh daemon. This can be done via terminal / PuTTy and then
 `sudo touch ssh`

4. Edit these files on the **OS partition**:
  * Edit `/etc/hostname` and `/etc/hosts` to change “raspberrypi” to a **unique host name**
    *  `sudo nano /etc/hostname` and `sudo nano /etc/hosts`
  * Edit `/etc/wpa_supplicant/wpa_supplicant.conf` to add your WiFi authentication:
    * `sudo nano `/etc/wpa_supplicant/wpa_supplicant.conf`

```
    network={
	    ssid="your WiFi name (SSID)"
	    psk="your WiFi password"
    }
```

5. Via Terminal or PuTTy (or similar), log into the raspberry pi and ensure it's up 2 date
 ```
 sudo apt-get update
 sudo apt-get upgrade
```


# Step 2: Create the hardware

1. Insert the microSD card into the Raspberry Pi.

2. Add the [WiFi dongle](https://www.adafruit.com/products/814) to Raspberry Pi USB port.  A Raspberry Pi Zero will need a [OTG Adapter adaptor](https://www.adafruit.com/product/2910).

3. Add the HTU21D-F Temperature & Humidity Sensor to [Raspberry Pi GPIO pins](https://pinout.xyz/). 

4. Plug in a power source, and you’re good to go.  Within a few seconds, you should be able to connect to the Pi with: “ssh pi@*{**unique host name**}*” (password: `raspberry`)



# Step 3: Create the software

After you ssh to the pi, install a few essential libraries:

    sudo apt-get --assume-yes install python-pip i2c-tools git python-smbus
    
Set the timezone to make sure timestamps are correct

    sudo raspi-config
    [Internationalisation Options]
    [Change Timezone]
    [Interfacing Options] --> [I2C] --> Enable / Yes

Clone the weatherSensor github repository

    sudo git clone https://github.com/ulnic/weatherSensor.git
    
Install weatherSensor dependencies (this includes [RPI.GPIO](https://pypi.python.org/pypi/RPi.GPIO) and [MQTT PAHO](https://github.com/eclipse/paho.mqtt.python))

    sudo pip install -r weatherSensor/install/requirements.txt

Set permissions in case of for all files and directories

    sudo chmod 755 -R *

Create the settings file `/home/pi/weatherSensor/config/configuration.ini`.  This file specifies what sensor pin to monitor, what messages you want, and what services to send the message to. 
Configure as per below:
* If first time, make a copy of `configuration.ini.sample` and call it `configuration.ini`. This file name is important
* Configure the sections and key-values accordingly. 

Edit `/etc/rc.local` to make the program run when the device boots up.

Add before the `exit` line:

    # Execute weather sensor automatically at start up
    sh /home/pi/weatherSensor/reboot_script_weatherSensor.sh 

You’re done!  Reboot and test it out.

# Step 4: (Optional) Setup [Home Assistant](https://home-assistant.io)

This weatherSensor works great with Home Assistant and a MQTT Broker.
Configure your Home Assistant yaml file similar to below:

    - platform: mqtt
      name: "Bedroom Temperature"
      state_topic: "weatherSensor/bedroom/rpi"
      value_template: '{{ value_json.temperature }}'
      unit_of_measurement: "Â°C"
      qos: 0

    - platform: mqtt
      name: "Bedroom Humidity"
      state_topic: "weatherSensor/bedroom/rpi"
      value_template: '{{ value_json.humidity }}'
      unit_of_measurement: "%"
      qos: 0

    - platform: mqtt
      name: "Bedroom CPU"
      state_topic: "weatherSensor/bedroom/rpi"
      value_template: '{{ value_json.cpu }}'
      unit_of_measurement: "C"
      qos: 0

    - platform: mqtt
      name: "Bedroom IP"
      state_topic: "weatherSensor/bedroom/rpi"
      value_template: '{{ value_json.ipaddress }}'
      qos: 0
   