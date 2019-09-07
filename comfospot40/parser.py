from threading import Thread
import logging
import struct
from .packet import Packet
from .state import State

class Parser(Thread):
    def __init__(self, serial):
        Thread.__init__(self)
        self._ser = serial
        self._state = State()

    def get_state(self):
        return self._state

    def search_length(self, data):
        logging.info('z')
        readbytes = self._ser.read(3)
        readints = struct.unpack("<BBB", readbytes)
        data.extend(readints)
        logging.info(readints)
        size = readints[-1]+1
        readbytes = self._ser.read(size)
        readints = struct.unpack("<"+"B"*(size), readbytes)
        data.extend(readints)
        logging.info(readints)
        z = Packet(data)
        pdata = [hex(d) for d in data]
        if z.checkcrc():
            if z.hassensordata():
                logging.debug(pdata, z.temperature(), z.humidity())
                self._state.addpacket(z)
            elif z.hasfandata():
                logging.debug(pdata, z.fannumber(), z.speed(), z.direction())
                self._state.addpacket(z)
            else:
                logging.warning("Unknown packet %s", pdata)
        else:
            logging.warning('Failed checksum %s', pdata)
        return data, self.search_preamble

    def search_preamble(self, data):
        logging.info('x')
        readbyte = self._ser.read()
        if not readbyte:
            return data, self.search_preamble
        readdata = struct.unpack("<B", readbyte)[0]
        logging.info(readdata)
        if readdata == 0x55:
            data = [0x55]
            return data, self.search_preamble2
        return data, self.search_preamble

    def search_preamble2(self, data):
        logging.info('y')
        readbyte = self._ser.read()
        if not readbyte:
            return data, self.search_preamble
        readdata = struct.unpack("<B", readbyte)[0]
        logging.info(readdata)
        if readdata in (0x4d, 0x00, 0x53):
            data.append(readdata)
            logging.info(data)
            return data, self.search_length
        if readdata == 0x55:
            return data, self.search_preamble2
        return data, self.search_preamble

    def run(self):
        parserstate = self.search_preamble
        data = []
        while True:
            data, parserstate = parserstate(data)
