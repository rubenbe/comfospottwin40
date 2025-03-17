import unittest
from comfospot40 import Counterfan
from comfospot40 import Fanspeed
from parameterized import parameterized_class


class TestCounterfan(unittest.TestCase):
    def test_default(self):
        f = Counterfan()
        self.assertEqual(f.value(), b"Always counter direction")
        self.assertTrue(f.on())

    def test_is_on_off(self):
        f = Counterfan()
        f.set_state(b"Off")
        self.assertEqual(f.value(), b"Off")
        self.assertFalse(f.on())

    def test_is_on_same(self):
        f = Counterfan()
        f.set_state(b"Always same direction")
        self.assertEqual(f.value(), b"Always same direction")
        self.assertTrue(f.on())

    def test_is_on_counter(self):
        f = Counterfan()
        f.set_state(b"Always counter direction")
        self.assertEqual(f.value(), b"Always counter direction")
        self.assertTrue(f.on())

    def test_is_on_oscillating(self):
        f = Counterfan()
        f.set_state(b"Counter when oscillating")
        self.assertEqual(f.value(), b"Counter when oscillating")
        self.assertTrue(f.on())

    def test_get_fan_speed_data_off(self):
        f = Counterfan()
        f.set_state(b"Off")
        z = Fanspeed()
        x = f.get_fan_data(z)
        self.assertEqual(x["speed"], 0)

    def test_get_fan_speed_data_on(self):
        f = Counterfan()
        f.set_state(b"Always same direction")
        z = Fanspeed()
        x = f.get_fan_data(z)
        self.assertEqual(x["speed"], 27)


@parameterized_class(
    [
        {
            "config": b"Always same direction",
            "mainfanfwd": True,
            "mainfanosc": False,
            "expected": True,
        },
        {
            "config": b"Always same direction",
            "mainfanfwd": False,
            "mainfanosc": False,
            "expected": False,
        },
        {
            "config": b"Always counter direction",
            "mainfanfwd": True,
            "mainfanosc": False,
            "expected": False,
        },
        {
            "config": b"Always counter direction",
            "mainfanfwd": False,
            "mainfanosc": False,
            "expected": True,
        },
        {
            "config": b"Counter when oscillating",
            "mainfanfwd": True,
            "mainfanosc": True,
            "expected": False,
        },
        {
            "config": b"Counter when oscillating",
            "mainfanfwd": False,
            "mainfanosc": True,
            "expected": True,
        },
        {
            "config": b"Counter when oscillating",
            "mainfanfwd": True,
            "mainfanosc": False,
            "expected": True,
        },
        {
            "config": b"Counter when oscillating",
            "mainfanfwd": False,
            "mainfanosc": False,
            "expected": False,
        },
    ]
)
class TestCounterfanDirection(unittest.TestCase):
    def test_get_fan_speed_direction(self):
        f = Counterfan()
        f.set_state(self.config)
        z = Fanspeed()
        z._direction_forward = self.mainfanfwd
        self.assertEqual(z.direction_forward(), self.mainfanfwd)
        z.set_oscillation(b"true" if self.mainfanosc else b"false")
        x = f.get_fan_data(z)
        self.assertEqual(x["direction"], self.expected)
