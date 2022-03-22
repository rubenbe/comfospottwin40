import unittest
from comfospot40 import Temperature


class TestTemperature(unittest.TestCase):
    def test_temperature1(self):
        t = Temperature()
        self.assertEqual(t.temperature(), None)

    def test_temperature2(self):
        t = Temperature()
        t.set_temperature(33)
        self.assertEqual(t.temperature(), 33)

    def test_mqtt_config1(self):
        t = Temperature()
        c = t.mqtt_config(0, "recycled")
        self.assertEqual(
            c,
            {
                "name": "Comfospot40 Zone 0 Recycled temperature",
                "command_topic": "comfospot40/zones/zone0/disabled",
                "device_class": "temperature",
                "state_class": "measurement",
                "state_topic": "comfospot40/zones/zone0/recycled_temperature",
                "temperature_unit": "celcius",
            },
        )

    def test_mqtt_config2(self):
        t = Temperature()
        c = t.mqtt_config(1, "inside")
        self.assertEqual(
            c,
            {
                "name": "Comfospot40 Zone 1 Inside temperature",
                "command_topic": "comfospot40/zones/zone1/disabled",
                "device_class": "temperature",
                "state_class": "measurement",
                "state_topic": "comfospot40/zones/zone1/inside_temperature",
                "temperature_unit": "celcius",
            },
        )

    def test_mqtt_compare1(self):
        t1 = Temperature()
        t1.set_temperature(30)
        t2 = Temperature()
        t2.set_temperature(30)
        self.assertEqual(t1, t2)

    def test_mqtt_compare2(self):
        t1 = Temperature()
        t1.set_temperature(30)
        t2 = Temperature()
        t2.set_temperature(31)
        self.assertNotEqual(t1, t2)
