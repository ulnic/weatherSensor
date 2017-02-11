#!/usr/bin/python
import logging
import subprocess
from subprocess import check_output
from data.SensorEnum import SensorType
from re import findall

logger = logging.getLogger('sensorLogger')


class Sensor(object):
    def __init__(self, sensor_type, read_sensor, sensor_message_topic, calibration_value=0, use_mock_sensor=False, gpiopin=-1):
        self.type = sensor_type
        self.readSensorToggle = read_sensor
        self.messageTopic = sensor_message_topic
        self.sensorValue = 0
        self.calibrationValue = calibration_value
        self.useMockSensor = use_mock_sensor
        self.gpioPin = gpiopin

        if self.type == SensorType.TEMPERATURE or self.type == SensorType.HUMIDITY or self.type == SensorType.LIGHT:
            if use_mock_sensor:
                logger.warning("MOCK Readers enabled, please update the configuration file")
                from envLibrary.tempHumidity_lib_MOCK import HTU21D
                from envLibrary import photocell_lib_MOCK as photocell
            else:
                logger.debug("LIVE Readers on RPI used.")
                from envLibrary.tempHumidity_lib import HTU21D
                from envLibrary import photocell_lib as photocell

            self.readSensor = HTU21D()
            self.photoCellReader = photocell

    def read_sensor(self):
        logger.debug("read Toggle set to %s ", self.readSensorToggle)

        if self.readSensorToggle:
            logger.debug("Reading Sensor")
            if self.type == SensorType.TEMPERATURE:
                self.sensorValue = float("{0:.1f}".format(self.readSensor.read_temperature() + self.calibrationValue))
                logger.info("Temperature Reading is: %s", format(self.sensorValue))

            elif self.type == SensorType.HUMIDITY:
                self.sensorValue = float("{0:.1f}".format(self.readSensor.read_humidity() + self.calibrationValue))
                logger.info("Humidity Reading is: %s", format(self.sensorValue))

            elif self.type == SensorType.LIGHT:
                self.sensorValue = float(
                    "{0:.0f}".format(self.photoCellReader.photocellRead(self.gpioPin) + self.calibrationValue))
                logger.info("Light Reading is: %s", format(self.sensorValue))

            elif self.type == SensorType.CPU:
                self.sensorValue = self.get_cpu_temp()
                # try:
                #     cpu_sensorValue = subprocess.call(['/opt/vc/bin/vcgencmd measure_temp > /dev/null 2> /dev/null'],
                #                                    shell=True)
                #     logger.debug('/opt/vc/bin/vcgencmd measure_temp RETURNED [%s]', cpu_sensorValue)
                #     self.sensorValue = float("{0:.1f}".format(cpu_sensorValue[5:]))
                # except Exception as e:
                #     logger.warn("Could not read CPU, setting to 0")
                logger.info("CPU Temperature Reading is %s", self.sensorValue)

            elif self.type == SensorType.LOCAL_IP:
                self.sensorValue = "1.2.3.4"
                try:
                    self.sensorValue = subprocess.call(
                        ['ifconfig wlan0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1 > /dev/null 2> /dev/null'],
                        shell=True)
                    logger.debug('ifconfig wlan0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1 RETURNED [%s]', self.sensorValue)
                    if len(self.sensorValue) == 0:
                        self.sensorValue = 'error'

                except Exception as e:
                    logger.warn("Could not read IP, due to: %s", e.__str__())
                    self.sensorValue = 'error'

                logger.info("Local IP Address is %s", format(self.sensorValue))
        else:
            logger.debug("DISABLED - check the configuration file")

    def get_cpu_temp(self):
        temp = 0
        try:
            temp = check_output(["vcgencmd","measure_temp"]).decode("UTF-8")
            temp = float(findall("\d+\.\d+",temp)[0])
        except Exception as e:
            logger.warn("Could not read CPU, due to %s", e.__str__())

        return temp
