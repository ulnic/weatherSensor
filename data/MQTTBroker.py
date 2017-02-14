#!/usr/bin/python
import paho.mqtt.publish as publish


class MQTTBroker(object):

    def __init__(self, _mqtt_host, _mqtt_port, _mqtt_topic):
        self.mqtt_host = _mqtt_host
        self.mqtt_port = _mqtt_port
        self.mqtt_topic = _mqtt_topic

    def publish(self, _json_data):
        publish.single(self.mqtt_topic, _json_data, hostname=self.mqtt_host, port=self.mqtt_port, retain=True, qos=0)
