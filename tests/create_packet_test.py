import unittest
import comfospot40
from parameterized import parameterized_class


@parameterized_class(
    [
        # {"zone": 1, "intake": True, "speed": 25, "expected": "554d009603 00 02 19 ff"},
        # {"zone": 1, "intake": False, "speed": 27, "expected": "554d009603 01 01 1b fd"},
        # {"zone": 2, "intake": True, "speed": 25, "expected": "554d009603 02 02 19 fd"},
        # {"zone": 2, "intake": False, "speed": 27, "expected": "554d009603 03 01 1b fb"},
        {
            "zone": 1,
            "alt": False,
            "intake": False,
            "speed": 0x2F,
            "expected": "554d00960300012fea",
        },
        {
            "zone": 1,
            "alt": False,
            "intake": True,
            "speed": 0x2C,
            "expected": "554d00960300022cec",
        },
        {
            "zone": 2,
            "alt": False,
            "intake": False,
            "speed": 0x2F,
            "expected": "554d00960302012fe8",
        },
        {
            "zone": 2,
            "alt": False,
            "intake": True,
            "speed": 0x2C,
            "expected": "554d00960302022cea",
        },
        {
            "zone": 3,
            "alt": False,
            "intake": False,
            "speed": 0x2F,
            "expected": "554d00960304012fe6",
        },
        {
            "zone": 3,
            "alt": False,
            "intake": True,
            "speed": 0x2C,
            "expected": "554d00960304022ce8",
        },
        {
            "zone": 1,
            "alt": True,
            "intake": False,
            "speed": 0x2F,
            "expected": "554d00970300012fe9",
        },
        {
            "zone": 1,
            "alt": True,
            "intake": True,
            "speed": 0x2C,
            "expected": "554d00970300022ceb",
        },
        {
            "zone": 2,
            "alt": True,
            "intake": False,
            "speed": 0x2F,
            "expected": "554d00970302012fe7",
        },
        {
            "zone": 2,
            "alt": True,
            "intake": True,
            "speed": 0x2C,
            "expected": "554d00970302022ce9",
        },
        {
            "zone": 3,
            "alt": True,
            "intake": False,
            "speed": 0x2F,
            "expected": "554d00970304012fe5",
        },
    ]
)
class TestParser(unittest.TestCase):
    def parsedata(self, datastring):
        packet = datastring.replace(" ", "")
        self.assertEqual(0, len(packet) % 2)
        msb = packet[::2]
        lsb = packet[1::2]
        return [int("".join(x), 16) for x in zip(msb, lsb)]

    def test_packet(self):
        self.assertEqual(
            self.parsedata(self.expected),
            comfospot40.create_speed_packet(
                self.zone, self.intake, self.speed, 0, self.alt
            ),
        )

    def test_crc(self):
        self.assertTrue(
            comfospot40.create_speed_packet(
                self.zone, self.intake, self.speed, 0, self.alt
            )
        )
