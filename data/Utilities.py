#!/usr/bin/python
"""
All Shared / Common utilities implemented here
"""


def str_to_bool(_str):
    """
    Converts any string value to a boolean by checking if equal to false
    :param _str: String to convert to bool
    :return: False if _str=False (case IN-sensitive), otherwise True
    """
    value = False
    if _str.lower() != 'false':
        value = True
    return value


# def reboot_if_no_recent_publish():
#     """
#     This checks when the last MQTT publish occured. IF older than 3x the configuration value
#     for the key [APP] polling_interval, then it will trigger a reboot
#     :return:
#     """
#
#     try:
#         import logging
#         from data.ConfigurationReader import ConfigurationReader
#         from data.Constants import Constant
#         import data.AppContext
#         from datetime import timedelta, datetime
#         import subprocess
#
#         logger = logging.getLogger(Constant.LOGGER_NAME)
#
#         cr = ConfigurationReader()
#         polling = cr.get_int_key_in_section(Constant.CONFIG_SECTION_APP, Constant.POLLING_INTERVAL)
#         use_mock_sensor = cr.get_bool_key_in_section(Constant.CONFIG_SECTION_APP, Constant.USE_MOCK_SENSOR)
#         max_no_publish_sec = (3 * polling) * -1
#
#         logger.debug("Last MQTT Publish attempt at {0}".format(data.AppContext.AppContext.to_string()))
#
#         if data.AppContext.AppContext.get_last_updated() < datetime.now() + timedelta(seconds=max_no_publish_sec):
#             if use_mock_sensor:
#                 cmd = 'sudo shutdown -r now'
#             else:
#                 cmd = 'echo REBOOT_TRIGGERED_BUT_IGNORED'
#
#             logger.warning(cmd)
#
#             try:
#                 subprocess.check_output(cmd, shell=True).rstrip('\n')
#             except Exception as cpe:
#                 logger.critical("Reboot failed with [{0}]".format(cpe.__str__()))
#
#     except ImportError as err:
#         print("FATAL ERROR, Could not import correct libraries in Utilities.reboot_if_no_recent_publish")
#         print("Error was [%s]".format(err.__str__()))


def reboot():
    """
    Reboots the pi unless use_mock_sensor is enabled in the configuration file
    :return:
    """

    try:
        import logging
        from data.ConfigurationReader import ConfigurationReader
        from data.Constants import Constant
        import subprocess

        logger = logging.getLogger(Constant.LOGGER_NAME)

        cr = ConfigurationReader()
        use_mock_sensor = cr.get_bool_key_in_section(Constant.CONFIG_SECTION_APP, Constant.USE_MOCK_SENSOR)

        if use_mock_sensor:
            cmd = 'echo REBOOT_TRIGGERED_BUT_IGNORED'
        else:
            cmd = 'sudo shutdown -r now'
            try:
                subprocess.check_output(cmd, shell=True).rstrip('\n')
            except Exception as cpe:
                logger.critical("Reboot failed with [{0}]".format(cpe.__str__()))

        logger.warning(cmd)

    except ImportError as err:
        print("FATAL ERROR, Could not import correct libraries in Utilities.reboot_if_no_recent_publish")
        print("Error was [%s]".format(err.__str__()))