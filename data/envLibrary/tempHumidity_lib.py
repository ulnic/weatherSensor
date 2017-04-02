#!/usr/bin/python
"""
Temperature & Humidity class
"""
import array
import time
import io
import fcntl

I2C_SLAVE = 0x0703

HTU21D_ADDR = 0x40  # HTU21D default address.
CMD_READ_TEMP_HOLD = "\xE3"
CMD_READ_HUM_HOLD = "\xE5"
CMD_READ_TEMP_NOHOLD = "\xF3"
CMD_READ_HUM_NOHOLD = "\xF5"
CMD_WRITE_USER_REG = "\xE6"
CMD_READ_USER_REG = "\xE7"
CMD_SOFT_RESET = "\xFE"

SHT31_I2CADDR = 0x44  # SHT31D default address
SHT31_SEND_MEASUREMENT = 0x2C  # Send measurement command, 0x2C(44)
SHT31_HIGH_REPEATABILITY = 0x06  # 0x06(06)	High repeatability measurement
SHT31_READ_DATA = 0x00  # Read data back from 0x00(00), 6 bytes


# noinspection PyMissingOrEmptyDocstring
class I2C(object):
    """
    I2C RPI Reader and writer class
    """

    def __init__(self, device, bus):
        self.fr = io.open("/dev/i2c-" + str(bus), "rb", buffering=0)
        self.fw = io.open("/dev/i2c-" + str(bus), "wb", buffering=0)

        # set device address
        fcntl.ioctl(self.fr, I2C_SLAVE, device)
        fcntl.ioctl(self.fw, I2C_SLAVE, device)

    def write(self, _bytes):
        self.fw.write(_bytes)

    def read(self, _bytes):
        return self.fr.read(_bytes)

    def close(self):
        self.fw.close()
        self.fr.close()


# noinspection PyMissingOrEmptyDocstring, PyMethodMayBeStatic
class HTU21D(object):
    """
    HTU21D-f from Adafruit class
    """

    def __init__(self):
        self.dev = I2C(HTU21D_ADDR, 1)  # HTU21D 0x40, bus 1
        self.dev.write(CMD_SOFT_RESET)  # soft reset
        time.sleep(.1)

    def ctemp(self, sensor_temp):
        t_sensor_temp = sensor_temp / 65536.0
        return -46.85 + (175.72 * t_sensor_temp)

    def chumid(self, sensor_humid):
        t_sensor_humid = sensor_humid / 65536.0
        return -6.0 + (125.0 * t_sensor_humid)

    def crc8check(self, value):
        # Ported from Sparkfun Arduino HTU21D Library: https://github.com/sparkfun/HTU21D_Breakout
        remainder = ((value[0] << 8) + value[1]) << 8
        remainder |= value[2]

        # POLYNOMIAL = 0x0131 = x^8 + x^5 + x^4 + 1
        # divisor = 0x988000 is the 0x0131 polynomial shifted to farthest left of three bytes
        divisor = 0x988000

        for i in range(0, 16):
            if remainder & 1 << (23 - i):
                remainder ^= divisor
            divisor >>= 1

        if remainder == 0:
            return True
        else:
            return False

    def read_temperature(self):
        self.dev.write(CMD_READ_TEMP_NOHOLD)  # measure temp
        time.sleep(.1)

        data = self.dev.read(3)
        buf = array.array('B', data)

        if self.crc8check(buf):
            temp = (buf[0] << 8 | buf[1]) & 0xFFFC
            return self.ctemp(temp)
        else:
            return -255

    def read_humidity(self):
        self.dev.write(CMD_READ_HUM_NOHOLD)  # measure humidity
        time.sleep(.1)

        data = self.dev.read(3)
        buf = array.array('B', data)

        if self.crc8check(buf):
            humid = (buf[0] << 8 | buf[1]) & 0xFFFC
            return self.chumid(humid)
        else:
            return -255


class SHT31(object):
    """
    SHT31-D (https://www.adafruit.com/products/2857) temperature and Humidity sensor.
    This class currently only extracts the temperature and humidity from the sensor.
    """

    def __init__(self, _address=SHT31_I2CADDR):
        self.bus = None  # Get I2C bus
        try:
            import smbus
            self.bus = smbus.SMBus(1)
            self.address = _address
        except ImportError as err:
            print("FATAL ERROR, Could not import SHT31 BUS libraries in tempHumidity_lib.py")
            print("Error was [%s]".format(str(err)))

    def read_temperature_humidity(self):
        """
        Core function which reads the sensors values, being both temperature and humidity. 
        :return: temperature, humidity
        """

        self.bus.write_i2c_block_data(self.address, SHT31_SEND_MEASUREMENT, [SHT31_HIGH_REPEATABILITY])
        time.sleep(0.5)

        # Read data back from 0x00(00), 6 bytes
        # Temp MSB, Temp LSB, Temp CRC, Humidity MSB, Humidity LSB, Humidity CRC
        data = self.bus.read_i2c_block_data(self.address, SHT31_READ_DATA, 6)

        # Convert the data
        raw_temperature = data[0] * 256 + data[1]
        temperature = -45 + (175 * raw_temperature / 65535.0)

        raw_humidity = data[3] * 256 + data[4]
        humidity = 100 * raw_humidity / 0xFFFF  # 0xFFFF is equivalent to 65535.0

        return temperature, humidity

    def read_temperature(self):
        """
        Extracts the temperature component from the sensor and returns the value
        :return: temperature (celsius)
        """
        (temperature, humidity) = self.read_temperature_humidity()
        return temperature

    def read_humidity(self):
        """
        Extracts the humidity component from the sensor and returns the value
        :return: humidity
        """
        (temperature, humidity) = self.read_temperature_humidity()
        return humidity
