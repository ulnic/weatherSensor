#!/usr/bin/python
"""
MQTT Broker
"""
import logging
import threading
import socket
import data.AppContext
from data.Constants import Constant
from data.Utilities import reboot
import paho.mqtt.publish as publish


logger = logging.getLogger(Constant.LOGGER_NAME)


class MQTTBroker(object):
    """
    Message MQTT Broker. Publish is only implemented currently.
    """

    def __init__(self, _mqtt_host, _mqtt_port, _mqtt_topic):
        self.mqtt_host = _mqtt_host
        self.mqtt_port = _mqtt_port
        self.mqtt_topic = _mqtt_topic

    def publish(self, _json_data):
        """
        Main MQTT Publish method which uses the configuration.ini defined topic, hostname and port to push messages
        :param _json_data: (str) containing the final json blurb to publish
        """

        # Setting up a new timer which will reboot the PI ONLY IF the following MQTT call does not complete
        # in 3 times the length of the polling interval.
        set_timer = 3 * data.AppContext.AppContext.get_polling_interval()

        t = threading.Timer(set_timer, reboot )
        t.setDaemon(True)
        t.start()

        logger.debug("BEFORE: MQTT Publish")
        publish.single(self.mqtt_topic, _json_data, hostname=self.mqtt_host, port=self.mqtt_port, retain=True, qos=0,
                       client_id=socket.gethostname())
        logger.debug("AFTER: Successfully ran MQTT Publish")

        t.cancel()     # Important to cancel the timer so that the reboot does NOT occur since successful

