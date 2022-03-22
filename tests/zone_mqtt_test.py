import unittest
from comfospot40 import *


class TestZoneMqtt(unittest.TestCase):
    def test_get_mqttconfig1(self):
        z = Zone()
        c = z.get_mqtt_config(0, True)
        self.assertNotEqual(c, {})
        c = z.get_mqtt_config(0, True)
        self.assertEqual(c, {})

    def test_get_mqttconfig2(self):
        z = Zone()
        c = z.get_mqtt_config(0, True)
        self.assertNotEqual(c, {})
        c = z.get_mqtt_config(0, False)
        self.assertEqual(c, {})

    def test_get_mqttconfig3(self):
        z = Zone()
        c = z.get_mqtt_config(0, False)
        self.assertNotEqual(c, {})
        c = z.get_mqtt_config(0, False)
        self.assertNotEqual(c, {})

    def test_get_mqttconfig4(self):
        z = Zone()
        c = z.get_mqtt_config(0, False)
        self.assertNotEqual(c, {})
        c = z.get_mqtt_config(0, True)
        self.assertNotEqual(c, {})
        c = z.get_mqtt_config(0, False)
        self.assertEqual(c, {})

    def test_get_mqttconfig_topics0(self):
        z = Zone()
        c = z.get_mqtt_config(0, False)
        k = list(c)
        k.sort()
        expected = [
            "homeassistant/fan/comfospot40/comfospot40_zone0/config",
            "homeassistant/sensor/comfospot40/comfospot40_zone0_temp_in/config",
            "homeassistant/sensor/comfospot40/comfospot40_zone0_temp_recycled/config",
            "homeassistant/sensor/comfospot40/comfospot40_zone0_humidity_in/config",
            "homeassistant/sensor/comfospot40/comfospot40_zone0_humidity_recycled/config",
        ]
        expected.sort()
        self.assertEqual(k, expected)

    def test_get_mqttconfig_topics1(self):
        z = Zone()
        c = z.get_mqtt_config(1, False)
        k = list(c)
        k.sort()
        expected = [
            "homeassistant/fan/comfospot40/comfospot40_zone1/config",
            "homeassistant/sensor/comfospot40/comfospot40_zone1_temp_in/config",
            "homeassistant/sensor/comfospot40/comfospot40_zone1_temp_recycled/config",
            "homeassistant/sensor/comfospot40/comfospot40_zone1_humidity_in/config",
            "homeassistant/sensor/comfospot40/comfospot40_zone1_humidity_recycled/config",
        ]
        expected.sort()
        self.assertEqual(k, expected)

    def test_get_mqttconfig_topic_zone(self):
        self.maxDiff = None
        z = Zone()
        c = z.get_mqtt_config(1, False)
        v = c["homeassistant/fan/comfospot40/comfospot40_zone1/config"]
        self.assertEqual(
            v,
            """{
                        "name": "Comfospot40 Zone 1",
                        "device_class": "fan",
                        "state_topic": "comfospot40/zones/zone1/state",
                        "percentage_state_topic": "comfospot40/zones/zone1/fan_speed",
                        "percentage_command_topic": "comfospot40/zones/zone1/fan_speed_todo",
                        "command_topic": "comfospot40/zones/zone1/set_fan_speed"}""",
        )

    def test_get_mqttconfig_topic_temp_in(self):
        self.maxDiff = None
        z = Zone()
        c = z.get_mqtt_config(2, False)
        v = c["homeassistant/sensor/comfospot40/comfospot40_zone2_temp_in/config"]
        self.assertEqual(
            v,
            """{"name": "Comfospot40 Zone 2 Inside temperature", "device_class": "temperature", "state_class": "measurement", "temperature_unit": "celcius", "state_topic": "comfospot40/zones/zone2/inside_temperature", "command_topic": "comfospot40/zones/zone2/disabled"}""",
        )

    def test_get_mqttconfig_topic_temp_recycled(self):
        self.maxDiff = None
        z = Zone()
        c = z.get_mqtt_config(3, False)
        v = c["homeassistant/sensor/comfospot40/comfospot40_zone3_temp_recycled/config"]
        self.assertEqual(
            v,
            """{"name": "Comfospot40 Zone 3 Recycled temperature", "device_class": "temperature", "state_class": "measurement", "temperature_unit": "celcius", "state_topic": "comfospot40/zones/zone3/recycled_temperature", "command_topic": "comfospot40/zones/zone3/disabled"}""",
        )

    def test_get_mqttconfig_topic_humidity_in(self):
        self.maxDiff = None
        z = Zone()
        c = z.get_mqtt_config(4, False)
        v = c["homeassistant/sensor/comfospot40/comfospot40_zone4_humidity_in/config"]
        self.assertEqual(
            v,
            """{
                        "name": "Comfospot40 Zone 4 Inside humidity",
                        "device_class": "humidity",
                        "state_class": "measurement",
                        "temperature_unit": "percentage",
                        "state_topic": "comfospot40/zones/zone4/inside_humidity",
                        "command_topic": "comfospot40/zones/zone4/disabled"}""",
        )

    def test_get_mqttconfig_topic_humidity_recycled(self):
        self.maxDiff = None
        z = Zone()
        c = z.get_mqtt_config(5, False)
        v = c[
            "homeassistant/sensor/comfospot40/comfospot40_zone5_humidity_recycled/config"
        ]
        self.assertEqual(
            v,
            """{
                        "name": "Comfospot40 Zone 5 Recycled humidity",
                        "device_class": "humidity",
                        "state_class": "measurement",
                        "temperature_unit": "percentage",
                        "state_topic": "comfospot40/zones/zone5/recycled_humidity",
                        "command_topic": "comfospot40/zones/zone5/disabled"}""",
        )