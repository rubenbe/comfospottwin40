import unittest
import comfospot40

sensorpackets={
        "55530098050102 2F 0119 C4":{"humidity":47},
        "55530098050102 11 020C EE":{"humidity":17},
        "55530098050102 44 00E1 E8":{"humidity":68},
        "55530098050102 3e 00F0 DF":{"humidity":62},
        "55530098050101 37 0109 CD":{"humidity":55},
        "55530098050101 37 010A CC":{"humidity":55}} # Sensor

fanpackets={
        "554D00960301020017": {}, "554D00960300010019": {},
        "554D00970301020016": {}, "554D00970300010018": {}, # Niveau 0 out?
        "554D009603010219FE": {}, "554D00960300011BFE": {},
        "554D00970300011BFD": {}, "554D009703010219FD": {}, # Niveau 1 out
        "554D00970301022CEA": {}, "554D00960300012FEA": {},
        "554D00960301022CEB": {}, "554D00970300012FE9": {}, # Niveau 2 out
        "554D00960301025DBA": {}, "554D009603000163B6": {},
        "554D009703000163B5": {}, "554D00970301025DB9": {}, # Niveau 4 out
        "554D00960301023CDB": {}, "554D00960300014ECB": {},
        "554D00970301023CDA": {}, "554D00970300014ECA": {}} # Niveau 3 out

class TestParser(unittest.TestCase):
    def test_valid_hassensordata(self):
        for packet, contents in sensorpackets.items():
            with self.subTest(packet=packet):
                packet = packet.replace(" ", "")
                self.assertEqual(0, len(packet)%2)
                msb=packet[::2]
                lsb=packet[1::2]
                packetbytes=[int(''.join(x),16) for x in zip(msb, lsb)]
                z = comfospot40.Packet(packetbytes)
                self.assertTrue(z.hassensordata())
                self.assertFalse(z.hasfandata())

    def test_valid_hasfandata(self):
        for packet, contents in fanpackets.items():
            with self.subTest(packet=packet):
                packet = packet.replace(" ", "")
                self.assertEqual(0, len(packet)%2)
                msb=packet[::2]
                lsb=packet[1::2]
                packetbytes=[int(''.join(x),16) for x in zip(msb, lsb)]
                z = comfospot40.Packet(packetbytes)
                self.assertTrue(z.hasfandata())
                self.assertFalse(z.hassensordata())

    def test_humiditydata(self):
        for packet, contents in sensorpackets.items():
            with self.subTest(packet=packet):
                packet = packet.replace(" ", "")
                self.assertEqual(0, len(packet)%2)
                msb=packet[::2]
                lsb=packet[1::2]
                packetbytes=[int(''.join(x),16) for x in zip(msb, lsb)]
                z = comfospot40.Packet(packetbytes)
                self.assertEqual(contents["humidity"], z.humidity())
