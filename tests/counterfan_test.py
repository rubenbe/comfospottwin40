import unittest
from comfospot40 import Counterfan
from comfospot40 import Zone


class TestFanspeed(unittest.TestCase):
    def test_default(self):
        f = Counterfan()
        self.assertEqual(f.value(), "Off")
        self.assertFalse(f.on())

    def test_is_on_off(self):
        f = Counterfan()
        f.set_state("Off")
        self.assertEqual(f.value(), "Off")
        self.assertFalse(f.on())

    def test_is_on_same(self):
        f = Counterfan()
        f.set_state("Always same direction")
        self.assertEqual(f.value(), "Always same direction")
        self.assertTrue(f.on())

    def test_is_on_counter(self):
        f = Counterfan()
        f.set_state("Always counter direction")
        self.assertEqual(f.value(), "Always counter direction")
        self.assertTrue(f.on())

    def test_is_on_oscillating(self):
        f = Counterfan()
        f.set_state("Counter when oscillating")
        self.assertEqual(f.value(), "Counter when oscillating")
        self.assertTrue(f.on())

    def test_get_fan_speed_data_off(self):
        f = Counterfan()
        f.set_state("Off")
        z = Zone()
        x = f.get_fan_data(z)
        self.assertEqual(x["speed"], 0)

    def test_get_fan_speed_data_on(self):
        f = Counterfan()
        f.set_state("Always same direction")
        z = Zone()
        x = f.get_fan_data(z)
        self.assertEqual(x["speed"], 27)
