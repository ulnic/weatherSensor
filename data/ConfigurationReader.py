#!/usr/bin/python
import logging
# noinspection PyCompatibility
from ConfigParser import SafeConfigParser

logger = logging.getLogger('sensorLogger')


class ConfigurationReader(object):
    def __init__(self):
        logger.debug('ConfigurationReader initialising ')

        logger.info('Reading  configurations from file')

        self.parser = SafeConfigParser()
        self.parser.read(['config/configuration.ini', '../config/configuration.ini'])

    def get_key_in_section(self, _section_name, _key_name):
        return self.parser.get(_section_name, _key_name)

    def get_all_section_names(self):
        """Returns a list of config section names."""
        return [m for m in self.parser.sections()]

    # def has_sensor_section(self, parser, _section_name):
    #     return parser.has_section(_section_name)

    def get_sensor_keys(self, _section_name):
        key_value_dict = {}
        for name, value in self.parser.items(_section_name):
            # logger.debug('%s = %s', name, value)
            key_value_dict[name] = value

        return key_value_dict
