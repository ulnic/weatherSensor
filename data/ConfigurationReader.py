#!/usr/bin/python
"""
Configuration Handler
"""
import logging
# noinspection PyCompatibility
import ConfigParser
import data.Constants

logger = logging.getLogger(data.Constants.Constant.LOGGER_NAME)


class ConfigurationReader(object):
    """
    Class handling the configuration parser from the configuration.ini file
    """
    def __init__(self):
        logger.info('Reading  configurations from file')

        self.parser = ConfigParser.SafeConfigParser()
        self.parser.read(data.Constants.Constant.CONFIG_FILE_NAME)

    def get_key_in_section(self, _section_name, _key_name):
        """
        Retrieves the specific KEY from the SECTION in the configuration.ini file
        :param _section_name: The CONFIG section to parse
        :param _key_name: The KEY in the config section to read
        :return: The value from the KEY inside the SECTION
        """
        return self.parser.get(_section_name, _key_name)

    def get_bool_key_in_section(self, _section_name, _key_name):
        """
        Retrieves and converts to INTEGER, the specific KEY from the SECTION in the configuration.ini file
        :param _section_name: The CONFIG section to parse
        :param _key_name: The KEY in the config section to read
        :return: The INTEGER value from the KEY inside the SECTION
        """
        return self.parser.getboolean(_section_name, _key_name)

    def get_int_key_in_section(self, _section_name, _key_name):
        """
        Retrieves and converts to BOOLEAN, the specific KEY from the SECTION in the configuration.ini file
        :param _section_name: The CONFIG section to parse
        :param _key_name: The KEY in the config section to read
        :return: The BOOLEAN value from the KEY inside the SECTION
        """
        return self.parser.getint(_section_name, _key_name)

    def get_all_section_names(self):
        """
        Returns a list of config section names.
        :return: List of all found sections in configuration.ini file.
        """
        return [m for m in self.parser.sections()]

    def has_sensor_section(self, _section_name):
        """
        Queries the config file and return bool indicating if section found
        :param _section_name: Section to search for
        :return: BOOL indicating if the section was found
        """
        return self.parser.has_section(_section_name)

    def get_sensor_keys(self, _section_name):
        """
        Retrieves all sensor keys under the section
        :param _section_name: Section in config file to get keys from
        :return: List of found key-values
        """
        key_value_dict = {}
        for name, value in self.parser.items(_section_name):
            key_value_dict[name] = value

        return key_value_dict
