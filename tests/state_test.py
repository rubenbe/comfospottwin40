import unittest
from comfospot40 import Packet, State


class TestState(unittest.TestCase):
    def parsedata(self, datastring):
        packet = datastring.replace(" ", "")
        self.assertEqual(0, len(packet) % 2)
        msb = packet[::2]
        lsb = packet[1::2]
        return [int("".join(x), 16) for x in zip(msb, lsb)]

    def test_zones_default(self):
        state = State()
        self.assertEqual({}, state.zones)

    def test_zones_add_zone1_fan(self):
        state = State()
        state.addpacket(Packet(self.parsedata("554D009603 00 01 1B FE")))
        self.assertTrue(1 in state.zones)
        self.assertEqual([1], list(state.zones.keys()))
        zone = state.zones[1]
        self.assertEqual(27, zone.fan_speed.value())
        self.assertEqual(False, zone.isintake)
