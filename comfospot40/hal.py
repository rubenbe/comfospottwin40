from comfospot40 import State, Parser
from comfospot40.create_packet import create_speed_packet
import serial_asyncio
import serial
import asyncio


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
            packet = create_speed_packet(
                zoneid, zonestate.fan_speed.direction_forward(), fan_speed, 0, 0
            )
            self._writer.write(bytes(packet))
            counter = zonestate.counter_fan.get_fan_data(zonestate.fan_speed)
            packet = create_speed_packet(
                zoneid, counter["direction"], counter["speed"], 1, 0
            )
            self._writer.write(bytes(packet))
            await asyncio.sleep(1)
