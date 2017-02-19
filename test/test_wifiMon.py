#!/usr/bin/python
"""
UNIT TEST Class
"""
from __future__ import absolute_import
from unittest import TestCase
import logging.config
from data.Constants import Constant
from data.wifiChecker.WifiMon import WifiMon


class TestWifiMon(TestCase):
    def setUp(self):
        self.logger = logging.getLogger(Constant.LOGGER_NAME)

    def test_wlan_check_success(self):
        wifi_monitor = WifiMon()
        wifi_monitor.use_mock_sensor = True
        wifi_monitor.WLAN_check_flg = True
        self.assertTrue(wifi_monitor.use_mock_sensor, "Setting USE MOCK SENSOR was not set to TRUE")
        self.assertTrue(wifi_monitor.WLAN_check_flg, "Setting WLAN_check_flg was not set to TRUE")
        self.assertEqual(1, wifi_monitor.wlan_check(), "String greater than 1 char, means Successful")

    def test_wlan_check_fail_sudo_reboot_path(self):
        wifi_monitor = WifiMon()
        wifi_monitor.use_mock_sensor = False
        wifi_monitor.WLAN_check_flg = True
        self.assertFalse(wifi_monitor.use_mock_sensor, "Setting USE MOCK SENSOR was not set to FALSE")
        self.assertTrue(wifi_monitor.WLAN_check_flg, "Setting WLAN_check_flg was not set to TRUE")
        self.assertEqual(wifi_monitor.wlan_check(), -1, "it works")

    def test_wlan_check_fail_wifi_power_cycle(self):
        wifi_monitor = WifiMon()
        wifi_monitor.use_mock_sensor = False
        wifi_monitor.WLAN_check_flg = False
        self.assertFalse(wifi_monitor.use_mock_sensor, "Setting USE MOCK SENSOR was not set to FALSE")
        self.assertFalse(wifi_monitor.WLAN_check_flg, "Setting WLAN_check_flg was not set to FALSE")
        self.assertEqual(wifi_monitor.wlan_check(), -2, "it works")
