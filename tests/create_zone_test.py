import unittest
import comfospot40
from parameterized import parameterized_class


@parameterized_class(
    [
        # {"zone": 1, "intake": True, "speed": 25, "expected": "554d009603 00 02 19 ff"},
        # {"zone": 1, "intake": False, "speed": 27, "expected": "554d009603 01 01 1b fd"},
        # {"zone": 2, "intake": True, "speed": 25, "expected": "554d009603 02 02 19 fd"},
        # {"zone": 2, "intake": False, "speed": 27, "expected": "554d009603 03 01 1b fb"},
        # {"zone": 1, "intake": True, "speed": 0, "expected": "554d009703 00 01 0018"},
        # {"zone": 1, "intake": True, "speed": 0, "expected": "554d009703 01 02 0016"},
        # {"zone": 2, "intake": True, "speed": 0, "expected": "554d009703 02 01 0016"},
        # {"zone": 2, "intake": True, "speed": 0, "expected": "554d009703 03 02 0014"},
        # {"zone": 3, "intake": True, "speed": 0, "expected": "554d009703 04 01 0014"},
        # {"zone": 3, "intake": True, "speed": 0, "expected": "554d009703 05 02 0012"},
        {"zone": 1, "intake": False, "speed": 0, "expected": "554d009603 00 01 0019"},
        {"zone": 1, "intake": True, "speed": 0, "expected": "554d009603 01 02 0017"},
        {"zone": 2, "intake": False, "speed": 0, "expected": "554d009603 02 01 0017"},
        {"zone": 2, "intake": True, "speed": 0, "expected": "554d009603 03 02 0015"},
        {"zone": 3, "intake": False, "speed": 0, "expected": "554d009603 04 01 0015"},
        {"zone": 3, "intake": True, "speed": 0, "expected": "554d009603 05 02 0013"},
    ]
)
class TestParser(unittest.TestCase):
    def parsedata(self, datastring):
        packet = datastring.replace(" ", "")
        self.assertEqual(0, len(packet) % 2)
        msb = packet[::2]
        lsb = packet[1::2]
        return [int("".join(x), 16) for x in zip(msb, lsb)]

    def test_zoneinfo(self):
        self.assertEqual(
            self.parsedata(self.expected),
            comfospot40.create_speed_packet(self.zone, self.intake, self.speed),
        )
