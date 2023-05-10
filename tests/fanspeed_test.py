import unittest
from comfospot40 import Fanspeed


class TestFanspeed(unittest.TestCase):
    def test_default_speed(self):
        f = Fanspeed()
        self.assertEqual(f.value(), 27)

    def test_preset_low(self):
        f = Fanspeed()
        f.set_preset(b"low")
        self.assertEqual(f.value(), 27)

    def test_preset_mid(self):
        f = Fanspeed()
        f.set_preset(b"mid")
        self.assertEqual(f.value(), 47)

    def test_preset_high(self):
        f = Fanspeed()
        f.set_preset(b"high")
        self.assertEqual(f.value(), 78)

    def test_preset_max(self):
        f = Fanspeed()
        f.set_preset(b"max")
        self.assertEqual(f.value(), 99)

    def test_preset_custom(self):
        f = Fanspeed()
        f.set_preset(b"custom")
        self.assertEqual(f.value(), 27, "Custom should have no effect")
