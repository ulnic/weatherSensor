#!/usr/bin/python
"""
MQTT Broker
"""
import logging
from data.Constants import Constant
import paho.mqtt.publish as publish
import data.AppContext

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
        data.AppContext.AppContext.update_last_time()

        logger.debug("Last MQTT Publish attempt at {0}".format(data.AppContext.AppContext.to_string()))
        publish.single(self.mqtt_topic, _json_data, hostname=self.mqtt_host, port=self.mqtt_port, retain=True, qos=0)
