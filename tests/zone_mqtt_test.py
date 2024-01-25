import unittest
from comfospot40 import Zone


class TestZoneMqtt(unittest.TestCase):
    def test_get_mqttconfig1(self):
        z = Zone()
        c = z.get_mqtt_config("a", 0, True)
        self.assertNotEqual(c, {})
        c = z.get_mqtt_config("a", 0, True)
        self.assertEqual(c, {})

    def test_get_mqttconfig2(self):
        z = Zone()
        c = z.get_mqtt_config("a", 0, True)
        self.assertNotEqual(c, {})
        c = z.get_mqtt_config("a", 0, False)
        self.assertEqual(c, {})

    def test_get_mqttconfig3(self):
        z = Zone()
        c = z.get_mqtt_config("a", 0, False)
        self.assertNotEqual(c, {})
        c = z.get_mqtt_config("a", 0, False)
        self.assertNotEqual(c, {})

    def test_get_mqttconfig4(self):
        z = Zone()
        c = z.get_mqtt_config("a", 0, False)
        self.assertNotEqual(c, {})
        c = z.get_mqtt_config("a", 0, True)
        self.assertNotEqual(c, {})
        c = z.get_mqtt_config("a", 0, False)
        self.assertEqual(c, {})

    def test_get_mqttconfig_topics0(self):
        z = Zone()
        c = z.get_mqtt_config("testspot42", 0, False)
        k = list(c)
        k.sort()
        expected = [
            "homeassistant/fan/testspot42_zone0_fan/config",
            "homeassistant/select/testspot42_zone0_counter/config",
            "homeassistant/sensor/testspot42/testspot42_zone0_temp_in/config",
            "homeassistant/sensor/testspot42/testspot42_zone0_temp_recycled/config",
            "homeassistant/sensor/testspot42/testspot42_zone0_humidity_in/config",
            "homeassistant/sensor/testspot42/testspot42_zone0_humidity_recycled/config",
        ]
        expected.sort()
        self.assertEqual(k, expected)

    def test_get_mqttconfig_topics1(self):
        z = Zone()
        c = z.get_mqtt_config("comfotest23", 1, False)
        k = list(c)
        k.sort()
        expected = [
            "homeassistant/fan/comfotest23_zone1_fan/config",
            "homeassistant/select/comfotest23_zone1_counter/config",
            "homeassistant/sensor/comfotest23/comfotest23_zone1_temp_in/config",
            "homeassistant/sensor/comfotest23/comfotest23_zone1_temp_recycled/config",
            "homeassistant/sensor/comfotest23/comfotest23_zone1_humidity_in/config",
            "homeassistant/sensor/comfotest23/comfotest23_zone1_humidity_recycled/config",
        ]
        expected.sort()
        self.assertEqual(k, expected)

    def test_get_mqttconfig_topic_zone(self):
        self.maxDiff = None
        z = Zone()
        c = z.get_mqtt_config("comfo40", 1, False)
        v = c["homeassistant/fan/comfo40_zone1_fan/config"]
        self.assertEqual(
            v,
            """{"name": "Comfospot40 Zone 1 Fan", """
            """"state_topic": "comfo40_zone1_fan/state", """
            """"command_topic": "comfo40_zone1_fan/on/set", """
            """"state_value_template": "{{ value_json.state }}", """
            """"direction_state_topic": "comfo40_zone1_fan/state", """
            """"direction_command_topic": "comfo40_zone1_fan/direction/set", """
            """"direction_value_template": "{{ value_json.direction }}", """
            """"oscillation_state_topic": "comfo40_zone1_fan/state", """
            """"oscillation_command_topic": "comfo40_zone1_fan/oscillation/set", """
            """"oscillation_value_template": "{{ value_json.oscillation }}", """
            """"percentage_state_topic": "comfo40_zone1_fan/state", """
            """"percentage_command_topic": "comfo40_zone1_fan/speed/percentage", """
            """"percentage_value_template": "{{ value_json.percentage }}", """
            """"preset_mode_state_topic": "comfo40_zone1_fan/state", """
            """"preset_mode_command_topic": "comfo40_zone1_fan/preset/set", """
            """"preset_mode_value_template": "{{ value_json.preset }}", """
            """"preset_modes": ["low", "mid", "high", "max", "custom"], """
            """"qos": 0, "payload_on": "true", "payload_off": "false", """
            """"payload_oscillation_on": "true", "payload_oscillation_off": "false", """
            """"unique_id": "comfo40_zone1_fan"}""",
        )

    def test_get_mqttconfig_topic_temp_in(self):
        self.maxDiff = None
        z = Zone()
        c = z.get_mqtt_config("comfo41", 2, False)
        v = c["homeassistant/sensor/comfo41/comfo41_zone2_temp_in/config"]
        self.assertEqual(
            v,
            """{"name": "Comfospot40 Zone 2 Inside temperature", """
            """"device_class": "temperature", "state_class": "measurement", """
            """"temperature_unit": "celcius", """
            """"state_topic": "comfo41/zones/zone2/inside_temperature"}""",
        )

    def test_get_mqttconfig_topic_temp_recycled(self):
        self.maxDiff = None
        z = Zone()
        c = z.get_mqtt_config("comfo42", 3, False)
        v = c["homeassistant/sensor/comfo42/comfo42_zone3_temp_recycled/config"]
        self.assertEqual(
            v,
            """{"name": "Comfospot40 Zone 3 Recycled temperature", """
            """"device_class": "temperature", "state_class": "measurement", """
            """"temperature_unit": "celcius", """
            """"state_topic": "comfo42/zones/zone3/recycled_temperature"}""",
        )

    def test_get_mqttconfig_topic_humidity_in(self):
        self.maxDiff = None
        z = Zone()
        c = z.get_mqtt_config("comfo43", 4, False)
        v = c["homeassistant/sensor/comfo43/comfo43_zone4_humidity_in/config"]
        self.assertEqual(
            v,
            """{"name": "Comfospot40 Zone 4 Inside humidity", """
            """"device_class": "humidity", "state_class": "measurement", """
            """"temperature_unit": "percentage", """
            """"state_topic": "comfo43/zones/zone4/inside_humidity"}""",
        )

    def test_get_mqttconfig_topic_humidity_recycled(self):
        self.maxDiff = None
        z = Zone()
        c = z.get_mqtt_config("comfo44", 5, False)
        v = c["homeassistant/sensor/comfo44/comfo44_zone5_humidity_recycled/config"]
        self.assertEqual(
            v,
            """{"name": "Comfospot40 Zone 5 Recycled humidity", """
            """"device_class": "humidity", "state_class": "measurement", """
            """"temperature_unit": "percentage", """
            """"state_topic": "comfo44/zones/zone5/recycled_humidity"}""",
        )
