#!/usr/bin/python


def str_to_bool(_str):
    value = False
    if _str.lower() != 'false':
        value = True
    return value