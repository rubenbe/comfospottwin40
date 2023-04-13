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
            "homeassistant/fan/comfospot40_zone0_fan/config",
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
            "homeassistant/fan/comfospot40_zone1_fan/config",
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
        v = c["homeassistant/fan/comfospot40_zone1_fan/config"]
        self.assertEqual(
            v,
            """{"name": "Comfospot40 Zone 1 Fan", "~": "comfospot40_zone1_fan", "state_topic": "comfospot40_zone1_fan/on/state", "command_topic": "~/on/set", "oscillation_state_topic": "comfospot40_zone1_fan/oscillation/state", "oscillation_command_topic": "~/oscillation/set", "percentage_state_topic": "comfospot40_zone1_fan/speed/percentage_state", "percentage_command_topic": "~/speed/percentage", "preset_mode_state_topic": "comfospot40_zone1_fan/preset/preset_mode_state", "preset_mode_command_topic": "~/preset/preset_mode", "preset_modes": ["in", "out", "in low", "low", "mid", "high", "max"], "qos": 0, "payload_on": "true", "payload_off": "false", "payload_oscillation_on": "true", "payload_oscillation_off": "false", "speed_range_min": 16, "speed_range_max": 128, "unique_id": "comfospot40_zone1_fan"}""",
        )

    def test_get_mqttconfig_topic_temp_in(self):
        self.maxDiff = None
        z = Zone()
        c = z.get_mqtt_config(2, False)
        v = c["homeassistant/sensor/comfospot40/comfospot40_zone2_temp_in/config"]
        self.assertEqual(
            v,
            """{"name": "Comfospot40 Zone 2 Inside temperature", "device_class": "temperature", "state_class": "measurement", "temperature_unit": "celcius", "state_topic": "comfospot40/zones/zone2/inside_temperature"}""",
        )

    def test_get_mqttconfig_topic_temp_recycled(self):
        self.maxDiff = None
        z = Zone()
        c = z.get_mqtt_config(3, False)
        v = c["homeassistant/sensor/comfospot40/comfospot40_zone3_temp_recycled/config"]
        self.assertEqual(
            v,
            """{"name": "Comfospot40 Zone 3 Recycled temperature", "device_class": "temperature", "state_class": "measurement", "temperature_unit": "celcius", "state_topic": "comfospot40/zones/zone3/recycled_temperature"}""",
        )

    def test_get_mqttconfig_topic_humidity_in(self):
        self.maxDiff = None
        z = Zone()
        c = z.get_mqtt_config(4, False)
        v = c["homeassistant/sensor/comfospot40/comfospot40_zone4_humidity_in/config"]
        self.assertEqual(
            v,
            """{"name": "Comfospot40 Zone 4 Inside humidity", "device_class": "humidity", "state_class": "measurement", "temperature_unit": "percentage", "state_topic": "comfospot40/zones/zone4/inside_humidity"}""",
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
            """{"name": "Comfospot40 Zone 5 Recycled humidity", "device_class": "humidity", "state_class": "measurement", "temperature_unit": "percentage", "state_topic": "comfospot40/zones/zone5/recycled_humidity"}""",
        )
