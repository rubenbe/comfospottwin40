import unittest
import comfospot40
from parameterized import parameterized_class


packets = []


@parameterized_class(
    [
        {"zone": 1, "intake": True, "speed": 25, "expected": "554D009603 01 02 19 FE"},
        {"zone": 1, "intake": False, "speed": 27, "expected": "554D009603 00 01 1B FE"},
        {"zone": 2, "intake": True, "speed": 27, "expected": "554D009603 02 02 1B FB"},
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
            comfospot40.CreatePacket.create_speed_packet(
                self.zone, self.intake, self.speed
            ),
        )

    def test_crc(self):
        self.assertTrue(
            comfospot40.CreatePacket.create_speed_packet(
                self.zone, self.intake, self.speed
            )
        )
