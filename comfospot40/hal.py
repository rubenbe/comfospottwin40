from comfospot40 import State, Parser
from comfospot40.create_packet import create_speed_packet
import serial_asyncio
import serial


class Hal:
    async def setup(self, devpath: str):
        self._reader, self._writer = await serial_asyncio.open_serial_connection(
            url=devpath, baudrate=2400, parity=serial.PARITY_NONE
        )
        Parser(self._reader, None)

    async def sendState(self, state: State):
        print("sendState")
        for zoneid, zonestate in state.zones.items():
            fan_speed = zonestate.fan_speed.serial_fan_speed()
            print(zoneid, fan_speed)
            packet = create_speed_packet(zoneid, True, fan_speed, 0, 0)
            self._writer.write(bytes(packet))
