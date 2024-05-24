import logging
import struct
import copy
import asyncio
from datetime import datetime
from serial import SerialException
from .packet import Packet
from .state import State


class Parser:
    def __init__(self, serial, packetlog=None, state=State()):
        self._ser = serial
        self._state = state
        self._packetlog = packetlog

        self.parserdata = []
        self.parserstate = self.search_preamble

    def get_state(self):
        return self._state

    async def read_byte(self, retries=5):
        while True:
            try:
                return await self._ser.read(1)
            except SerialException as e:
                logging.warning("Failed to read serial: {}".format(e))
                if retries > 0:
                    await asyncio.sleep(0.1 * retries)
                    retries -= 1
                else:
                    raise e

    async def search_length(self, data):
        logging.info("z")
        readbytes = b""
        while len(readbytes) < 3:
            readbytes += await self.read_byte()
        readints = struct.unpack("<BBB", readbytes)
        data.extend(readints)
        logging.info(readints)
        size = readints[-1] + 1
        readbytes = b""
        while len(readbytes) < size:
            readbytes += await self.read_byte()
        readints = struct.unpack("<" + "B" * (size), readbytes)
        data.extend(readints)
        logging.info(readints)
        z = Packet(data)
        pdata = [hex(d) for d in data]
        if self._packetlog:
            with open(self._packetlog, "a") as logfile:
                logfile.write(
                    datetime.now().strftime("%H:%M:%S.%f") + "  " + str(z) + "\n"
                )
        if True:  # z.checkcrc():
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
        readbyte = await self.read_byte()
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
        readbyte = await self.read_byte()
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
        state = copy.deepcopy(self._state)
        while self._state == state:
            self.parserdata, self.parserstate = await self.parserstate(self.parserdata)
        return self._state
