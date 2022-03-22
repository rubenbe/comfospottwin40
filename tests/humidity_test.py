import unittest
from comfospot40 import Humidity


class TestHumidity(unittest.TestCase):
    def test_temperature1(self):
        t = Humidity()
        self.assertEqual(t.humidity(), None)

    def test_temperature2(self):
        t = Humidity()
        t.set_humidity(33)
        self.assertEqual(t.humidity(), 33)

    def test_mqtt_config1(self):
        t = Humidity()
        c = t.mqtt_config(0, "recycled")
        self.assertEqual(
            c,
            {
                "name": "Comfospot40 Zone 0 Recycled humidity",
                "command_topic": "comfospot40/zones/zone0/disabled",
                "device_class": "humidity",
                "state_class": "measurement",
                "state_topic": "comfospot40/zones/zone0/recycled_humidity",
                "temperature_unit": "percentage",
            },
        )

    def test_mqtt_config2(self):
        t = Humidity()
        c = t.mqtt_config(1, "inside")
        self.assertEqual(
            c,
            {
                "name": "Comfospot40 Zone 1 Inside humidity",
                "command_topic": "comfospot40/zones/zone1/disabled",
                "device_class": "humidity",
                "state_class": "measurement",
                "state_topic": "comfospot40/zones/zone1/inside_humidity",
                "temperature_unit": "percentage",
            },
        )

    def test_mqtt_compare1(self):
        t1 = Humidity()
        t1.set_humidity(30)
        t2 = Humidity()
        t2.set_humidity(30)
        self.assertEqual(t1, t2)

    def test_mqtt_compare2(self):
        t1 = Humidity()
        t1.set_humidity(30)
        t2 = Humidity()
        t2.set_humidity(31)
        self.assertNotEqual(t1, t2)
