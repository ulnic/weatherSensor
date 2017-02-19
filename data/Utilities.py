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
