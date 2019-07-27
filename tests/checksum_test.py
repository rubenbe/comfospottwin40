import unittest
import comfospot40

packets=["555300980501022F0119C4", "5553009805010211020CEE", "555300980501024400E1E8", "555300980501023e00F0DF", "55530098050101370109CD", "5553009805010137010ACC"] # Sensor

packets+=["554D00960301020017", "554D00960300010019",
        "554D00970301020016", "554D00970300010018"] # Niveau 0 out?
packets+=["554D009603010219FE", "554D00960300011BFE",
        "554D00970300011BFD", "554D009703010219FD"] # Niveau 1 out
packets+=["554D00970301022CEA", "554D00960300012FEA",
        "554D00960301022CEB", "554D00970300012FE9"] # Niveau 2 out
packets+=["554D00960301025DBA", "554D009603000163B6",
        "554D009703000163B5", "554D00970301025DB9"] # Niveau 4 out
packets+=["554D00960301023CDB", "554D00960300014ECB",
        "554D00970301023CDA", "554D00970300014ECA"] # Niveau 3 out

class TestStringMethods(unittest.TestCase):
    def test_checksum(self):
        for packet in packets:
            with self.subTest(packet=packet):
                self.assertEqual(0, len(packet)%2)
                msb=packet[::2]
                lsb=packet[1::2]
                packetbytes=[int(''.join(x),16) for x in zip(msb, lsb)]
                z = comfospot40.Packet(packetbytes)
                self.assertTrue(z.checkcrc())
