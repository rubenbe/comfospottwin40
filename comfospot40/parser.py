import logging
import struct
from .packet import Packet
from .state import State


class Parser:
    def __init__(self, serial):
        self._ser = serial
        self._state = State()

        self.parserdata = []
        self.parserstate = self.search_preamble

    def get_state(self):
        return self._state

    async def search_length(self, data):
        logging.info("z")
        readbytes = b""
        while len(readbytes) < 3:
            readbytes += await self._ser.read(1)
        readints = struct.unpack("<BBB", readbytes)
        data.extend(readints)
        logging.info(readints)
        size = readints[-1] + 1
        readbytes = b""
        while len(readbytes) < size:
            readbytes += await self._ser.read(1)
        readints = struct.unpack("<" + "B" * (size), readbytes)
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
            logging.warning("Failed checksum %s", pdata)
        return data, self.search_preamble

    async def search_preamble(self, data):
        logging.info("x")
        readbyte = await self._ser.read(1)
        if not readbyte:
            return data, self.search_preamble
        readdata = struct.unpack("<B", readbyte)[0]
        logging.info(readdata)
        if readdata == 0x55:
            data = [0x55]
            return data, self.search_preamble2
        return data, self.search_preamble

    async def search_preamble2(self, data):
        logging.info("y")
        readbyte = await self._ser.read(1)
        if not readbyte:
            return data, self.search_preamble
        readdata = struct.unpack("<B", readbyte)[0]
        logging.info(readdata)
        if readdata in (0x4D, 0x00, 0x53):
            data.append(readdata)
            logging.info(data)
            return data, self.search_length
        if readdata == 0x55:
            return data, self.search_preamble2
        return data, self.search_preamble

    async def run(self):
        self.parserdata, self.parserstate = await self.parserstate(self.parserdata)
        return self._state
