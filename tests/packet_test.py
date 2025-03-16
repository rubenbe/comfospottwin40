import unittest
import comfospot40

sensorpackets = {
    "5553009805 01 02 2F 0119 C4": {
        "humidity": 47,
        "temperature": 28.1,
        "zone": 1,
        "direction": 2,
    },
    "5553009805 01 02 11 020C EE": {
        "humidity": 17,
        "temperature": 52.4,
        "zone": 1,
        "direction": 2,
    },
    "5553009805 01 02 44 00E1 E8": {
        "humidity": 68,
        "temperature": 22.5,
        "zone": 1,
        "direction": 2,
    },
    "5553009805 01 02 3e 00F0 DF": {
        "humidity": 62,
        "temperature": 24.0,
        "zone": 1,
        "direction": 2,
    },
    "5553009805 01 01 37 0109 CD": {
        "humidity": 55,
        "temperature": 26.5,
        "zone": 1,
        "direction": 1,
    },
    "5553009805 01 01 37 010A CC": {
        "humidity": 55,
        "temperature": 26.6,
        "zone": 1,
        "direction": 1,
    },
    "5553009805 04 02 3f 00ef dc": {
        "humidity": 63,
        "temperature": 23.9,
        "zone": 3,
        "direction": 2,
        "fan": 4,
    },
    "5553009805 03 01 5d 011a 94": {
        "humidity": 93,
        "temperature": 28.2,
        "zone": 2,
        "direction": 1,
        "fan": 3,
    },
    "5553009805 03 02 5b 0123 8c": {
        "humidity": 91,
        "temperature": 29.1,
        "zone": 2,
        "direction": 2,
        "fan": 3,
    },
    "5553009805 04 01 41 00eb df": {
        "humidity": 65,
        "temperature": 23.5,
        "zone": 3,
        "direction": 1,
        "fan": 4,
    },
    "5553009805 05 01 4e 012f 8c": {
        "temperature": 30.3,
        "humidity": 78.0,
        "direction": 1,
        "fan": 5,
        "intake": False,
    },
    "5553009805 04 02 2b 0101 dd": {
        "temperature": 25.7,
        "humidity": 43.0,
        "direction": 2,
        "fan": 4,
        "intake": True,
    },
    "5553009805 04 01 2b 0101 de": {
        "temperature": 25.7,
        "humidity": 43.0,
        "direction": 1,
        "fan": 4,
        "intake": False,
    },
    "5553009805 05 02 4b 012e 8f": {
        "temperature": 30.2,
        "humidity": 75.0,
        "direction": 2,
        "fan": 5,
        "intake": True,
    },
    "555300980500022f00ac33": {
        "temperature": 17.2,
        "humidity": 47,
        "direction": 2,
        "fan": 0,
        "intake": True,
    },
}

fanpackets = {
    # Niveau 0 out?
    "554D009603 01 02 00 17": {"zone": 1, "direction": 2},
    "554D009603 00 01 00 19": {"zone": 1, "direction": 1},
    "554D009703 01 02 00 16": {"zone": 1, "direction": 2},
    "554D009703 00 01 00 18": {"zone": 1, "direction": 1},
    # Niveau 1 out
    "554D009603 01 02 19 FE": {"zone": 1, "direction": 2},
    "554D009603 00 01 1B FE": {"zone": 1, "direction": 1},
    "554D009703 00 01 1B FD": {"zone": 1, "direction": 1},
    "554D009703 01 02 19 FD": {"zone": 1, "direction": 2},
    # Niveau 2 out
    "554D009703 01 02 2C EA": {"zone": 1, "direction": 2},
    "554D009603 00 01 2F EA": {"zone": 1, "direction": 1},
    "554D009603 01 02 2C EB": {"zone": 1, "direction": 2},
    "554D009703 00 01 2F E9": {"zone": 1, "direction": 1},
    # Niveau 4 out
    "554D009603 01 02 5D BA": {"zone": 1, "direction": 2},
    "554D009603 00 01 63 B6": {"zone": 1, "direction": 1},
    "554D009703 00 01 63 B5": {"zone": 1, "direction": 1},
    "554D009703 01 02 5D B9": {"zone": 1, "direction": 2},
    # Niveau 3 out
    "554D009603 01 02 3C DB": {"zone": 1, "direction": 2},
    "554D009603 00 01 4E CB": {"zone": 1, "direction": 1},
    "554D009703 01 02 3C DA": {"zone": 1, "direction": 2},
    "554D009703 00 01 4E CA": {"zone": 1, "direction": 1},
}

allpackets = {}
allpackets.update(sensorpackets)
allpackets.update(fanpackets)


class TestParser(unittest.TestCase):
    def parsedata(self, datastring):
        packet = datastring.replace(" ", "")
        self.assertEqual(0, len(packet) % 2)
        msb = packet[::2]
        lsb = packet[1::2]
        return [int("".join(x), 16) for x in zip(msb, lsb)]

    def parsepacket(self, packets, fieldname):
        return [
            (self.parsedata(data), fields[fieldname])
            for data, fields in packets.items()
            if fieldname in fields
        ]

    def test_valid_hassensordata(self):
        for packet, contents in sensorpackets.items():
            with self.subTest(packet=packet):
                packet = packet.replace(" ", "")
                self.assertEqual(0, len(packet) % 2)
                msb = packet[::2]
                lsb = packet[1::2]
                packetbytes = [int("".join(x), 16) for x in zip(msb, lsb)]
                z = comfospot40.Packet(packetbytes)
                self.assertTrue(z.hassensordata())
                self.assertFalse(z.hasfandata())

    def test_valid_hasfandata(self):
        for packet, contents in fanpackets.items():
            with self.subTest(packet=packet):
                packet = packet.replace(" ", "")
                self.assertEqual(0, len(packet) % 2)
                msb = packet[::2]
                lsb = packet[1::2]
                packetbytes = [int("".join(x), 16) for x in zip(msb, lsb)]
                z = comfospot40.Packet(packetbytes)
                self.assertTrue(z.hasfandata())
                self.assertFalse(z.hassensordata())

    def test_humiditydata(self):
        for packet, field in self.parsepacket(sensorpackets, "humidity"):
            with self.subTest(packet=packet):
                z = comfospot40.Packet(packet)
                self.assertEqual(field, z.humidity())

    def test_temperaturedata(self):
        for packet, field in self.parsepacket(sensorpackets, "temperature"):
            with self.subTest(packet=packet):
                z = comfospot40.Packet(packet)
                self.assertEqual(field, z.temperature())

    def test_zonedata(self):
        for packet, field in self.parsepacket(allpackets, "zone"):
            with self.subTest(packet=packet):
                z = comfospot40.Packet(packet)
                self.assertEqual(field, z.getzone())

    def test_directiondata(self):
        for packet, field in self.parsepacket(allpackets, "direction"):
            with self.subTest(packet=packet):
                z = comfospot40.Packet(packet)
                self.assertEqual(field, z.direction())

    def test_fannumberdata(self):
        for packet, field in self.parsepacket(allpackets, "fan"):
            with self.subTest(packet=packet):
                z = comfospot40.Packet(packet)
                self.assertEqual(field, z.fannumber())

    def test_intakedata(self):
        for packet, field in self.parsepacket(allpackets, "intake"):
            with self.subTest(packet=packet):
                z = comfospot40.Packet(packet)
                self.assertEqual(field, z.intake())
                self.assertEqual(field, not z.extract())
