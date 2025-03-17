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
        self.assertEqual(
            str(state.zones[1]), "🔀🏠➡️ ⬅️   0s (27 lo)🌡️ ____C, __% ♻️  ____C, __%"
        )
        self.assertEqual(
            str(state.zones[2]), "🔀🏠➡️ ⬅️   0s (27 lo)🌡️ ____C, __% ♻️  ____C, __%"
        )
        self.assertEqual(
            str(state.zones[3]), "🔀🏠➡️ ⬅️   0s (27 lo)🌡️ ____C, __% ♻️  ____C, __%"
        )

    def test_zones_add_zone1_fan(self):
        state = State()
        state.addpacket(Packet(self.parsedata("554D009603 00 01 1B FE")))
        self.assertTrue(1 in state.zones)
        self.assertEqual([1, 2, 3], list(state.zones.keys()))
        zone = state.zones[1]
        self.assertEqual(27, zone.fan_speed.value())
        self.assertEqual(False, zone.isintake)

    def test_zones_add_sensor_1(self):
        state = State()
        state.addpacket(Packet(self.parsedata("5553009805 01 02 44 00E1 E8")))
        zone = state.zones[1]
        self.assertEqual(22.5, zone.recycled_temperature.value())
        self.assertEqual(68, zone.recycled_humidity.value())
        self.assertEqual(None, zone.inside_temperature.value())
        self.assertEqual(None, zone.inside_humidity.value())

    def test_zones_add_sensor_2(self):
        state = State(reverse=True)
        state.addpacket(Packet(self.parsedata("5553009805 01 02 44 00E1 E8")))
        zone = state.zones[1]
        self.assertEqual(None, zone.recycled_temperature.value())
        self.assertEqual(None, zone.recycled_humidity.value())
        self.assertEqual(22.5, zone.inside_temperature.value())
        self.assertEqual(68, zone.inside_humidity.value())

    def test_zones_counter_fan_1(self):
        state = State()
        self.assertEqual(
            str(state.zones[1]), "🔀🏠➡️ ⬅️   0s (27 lo)🌡️ ____C, __% ♻️  ____C, __%"
        )

    def test_zones_counter_fan_2(self):
        state = State()
        zone = state.zones[1]
        zone.counter_fan.set_state(b"Always same direction")
        self.assertEqual(str(zone), "🔀🏠➡️ ➡️   0s (27 lo)🌡️ ____C, __% ♻️  ____C, __%")

    def test_zones_counter_fan_3(self):
        state = State()
        zone = state.zones[1]
        zone.counter_fan.set_state(b"Always counter direction")
        self.assertEqual(str(zone), "🔀🏠➡️ ⬅️   0s (27 lo)🌡️ ____C, __% ♻️  ____C, __%")

    def test_zones_counter_fan_4(self):
        state = State()
        zone = state.zones[1]
        zone.counter_fan.set_state(b"Counter when oscillating")
        self.assertEqual(str(zone), "🔀🏠➡️ ⬅️   0s (27 lo)🌡️ ____C, __% ♻️  ____C, __%")

    def test_zones_counter_fan_5(self):
        state = State()
        zone = state.zones[1]
        zone.counter_fan.set_state(b"Off")
        self.assertEqual(str(zone), "🔀🏠➡️ ⏸️   0s (27 lo)🌡️ ____C, __% ♻️  ____C, __%")

    def test_zones_counter_fan_6(self):
        state = State()
        zone = state.zones[1]
        zone.fan_speed.set_on(b"false")
        zone.counter_fan.set_state(b"Always same direction")
        self.assertEqual(str(zone), "🔀🏠⏸️ ⏸️   0s (27 lo)🌡️ ____C, __% ♻️  ____C, __%")

    def test_zones_not_oscillating(self):
        state = State()
        zone = state.zones[1]
        zone.fan_speed.set_oscillation(b"false")
        zone.fan_speed.set_on(b"false")
        self.assertEqual(str(zone), "  🏠⏸️ ⏸️   0s (27 lo)🌡️ ____C, __% ♻️  ____C, __%")
