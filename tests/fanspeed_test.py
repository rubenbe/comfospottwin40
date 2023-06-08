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
        self.assertEqual(f.value(), 100)

    def test_preset_custom(self):
        f = Fanspeed()
        f.set_preset(b"custom")
        self.assertEqual(f.value(), 27, "Custom should have no effect")

    def test_value_low(self):
        f = Fanspeed()
        f.set_fan_speed(27)
        self.assertEqual(f.preset(), "low")

    def test_value_mid(self):
        f = Fanspeed()
        f.set_fan_speed(47)
        self.assertEqual(f.preset(), "mid")

    def test_value_high(self):
        f = Fanspeed()
        f.set_fan_speed(78)
        self.assertEqual(f.preset(), "high")

    def test_value_max(self):
        f = Fanspeed()
        f.set_fan_speed(100)
        self.assertEqual(f.preset(), "max")

    def test_value_custom(self):
        f = Fanspeed()
        f.set_fan_speed(42)
        self.assertEqual(f.preset(), "custom")

    def test_off(self):
        f = Fanspeed()
        f.set_fan_speed(42)
        self.assertEqual(True, f.on())
        self.assertEqual(42, f.fan_speed())
        self.assertEqual(42, f.serial_fan_speed())
        f.set_on(b"false")
        self.assertEqual(False, f.on())
        self.assertEqual(42, f.fan_speed())
        self.assertEqual(0, f.serial_fan_speed())
        f.set_on(b"true")
        self.assertEqual(True, f.on())
        self.assertEqual(42, f.fan_speed())
        self.assertEqual(42, f.serial_fan_speed())

    def test_snap_to_off(self):
        f = Fanspeed()
        f.set_fan_speed(42)
        self.assertEqual(True, f.on())
        self.assertEqual(42, f.fan_speed())
        self.assertEqual(42, f.serial_fan_speed())
        f.set_fan_speed(9)
        self.assertEqual(False, f.on())
        self.assertEqual(42, f.fan_speed())
        self.assertEqual(0, f.serial_fan_speed())
        f.set_on(b"true")
        self.assertEqual(True, f.on())
        self.assertEqual(42, f.fan_speed())
        self.assertEqual(42, f.serial_fan_speed())

    def test_snap_to_minimum(self):
        f = Fanspeed()
        f.set_fan_speed(42)
        self.assertEqual(True, f.on())
        self.assertEqual(42, f.fan_speed())
        self.assertEqual(42, f.serial_fan_speed())
        f.set_fan_speed(10)
        self.assertEqual(True, f.on())
        self.assertEqual(27, f.fan_speed())
        self.assertEqual(27, f.serial_fan_speed())

    def test_set_direction_forward(self):
        f = Fanspeed()
        f.set_direction(b"forward")
        self.assertTrue(f.direction_forward())

    def test_set_direction_reverse(self):
        f = Fanspeed()
        f.set_direction(b"reverse")
        self.assertFalse(f.direction_forward())

    def test_set_oscillation_true(self):
        f = Fanspeed()
        f.set_oscillation(b"true")
        self.assertTrue(f.oscillating())

    def test_set_oscillation_false(self):
        f = Fanspeed()
        f.set_oscillation(b"false")
        self.assertFalse(f.oscillating())

    def test_switch_not_oscillation(self):
        f = Fanspeed()
        f.set_direction(b"forward")
        f.set_oscillation(b"false")
        f.maybe_switch_direction()
        self.assertTrue(f.direction_forward())

    def test_switch_when_oscillation(self):
        f = Fanspeed()
        f.set_direction(b"forward")
        f.set_oscillation(b"true")
        f.maybe_switch_direction()
        self.assertFalse(f.direction_forward())
