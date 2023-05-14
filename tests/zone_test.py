import unittest
from comfospot40 import Zone


class TestZone(unittest.TestCase):
    def test_zones_Empty(self):
        self.assertEqual(Zone(), Zone())

    def test_zones_Eq_IgnoreTime(self):
        z1 = Zone()
        z1.recycled_temperature.set_temperature(10)
        z1.timer = 10
        z2 = Zone()
        z2.recycled_temperature.set_temperature(10)
        z2.timer = 11
        self.assertEqual(z1, z2)

    def test_zones_Eq_Temperature(self):
        z1 = Zone()
        z1.inside_temperature.set_temperature(10)
        z2 = Zone()
        z2.inside_temperature.set_temperature(10)
        self.assertEqual(z1, z2)

    def test_zones_Neq_Temperature(self):
        z1 = Zone()
        z1.inside_temperature.set_temperature(10)
        z2 = Zone()
        z2.inside_temperature.set_temperature(11)
        self.assertNotEqual(z1, z2)

    def test_zones_Eq_RecycledTemperature(self):
        z1 = Zone()
        z1.recycled_temperature.set_temperature(10)
        z2 = Zone()
        z2.recycled_temperature.set_temperature(10)
        self.assertEqual(z1, z2)

    def test_zones_Neq_RecycledTemperature(self):
        z1 = Zone()
        z1.recycled_temperature.set_temperature(10)
        z2 = Zone()
        z2.recycled_temperature.set_temperature(11)
        self.assertNotEqual(z1, z2)

    def test_zones_Neq_FanSpeed(self):
        z1 = Zone()
        z1.fan_speed.set_fan_speed(42)
        z2 = Zone()
        z2.fan_speed.set_fan_speed(43)
        self.assertNotEqual(z1, z2)

    def test_zones_Eq_FanSpeed(self):
        z1 = Zone()
        z1.fan_speed.set_fan_speed(42)
        z2 = Zone()
        z2.fan_speed.set_fan_speed(42)
        self.assertEqual(z1, z2)

    def test_zones_Neq_IsIntake(self):
        z1 = Zone()
        z1.isintake = True
        z2 = Zone()
        z2.isintake = False
        self.assertNotEqual(z1, z2)

    def test_zones_Eq_IsIntake(self):
        z1 = Zone()
        z1.isintake = True
        z2 = Zone()
        z2.isintake = True
        self.assertEqual(z1, z2)
