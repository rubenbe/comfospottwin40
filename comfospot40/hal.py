from comfospot40 import State, Parser
from comfospot40.create_packet import create_speed_packet
import serial_asyncio
import serial
import asyncio
import time


class Hal:
    def __init__(self, state, oscillation_time):
        self._state = state
        self._oscillation_time = oscillation_time
        self._oscillation_switch = time.monotonic()

    async def setup(self, devpath: str):
        self._reader, self._writer = await serial_asyncio.open_serial_connection(
            url=devpath, baudrate=2400, parity=serial.PARITY_NONE
        )
        self.parser = Parser(self._reader, None, self._state)

    async def sendState(self, state: State):
        timer = time.monotonic()
        switch_dir = (timer - self._oscillation_switch) > self._oscillation_time
        print("sendState", timer, switch_dir)
        if switch_dir:
            self._oscillation_switch = timer
        for zoneid, zonestate in state.zones.items():
            fan_speed = zonestate.fan_speed.serial_fan_speed()
            print(zoneid, fan_speed)
            if switch_dir:
                zonestate.fan_speed.maybe_switch_direction()
            packet = create_speed_packet(
                zoneid, zonestate.fan_speed.direction_forward(), fan_speed, 0, True
            )
            self._writer.write(bytes(packet))
            await asyncio.sleep(0.5)
            counter = zonestate.counter_fan.get_fan_data(zonestate.fan_speed)
            print(counter["direction"], counter["speed"])
            packet = create_speed_packet(
                zoneid, counter["direction"], counter["speed"], 1, True
            )
            print("Writing")
            self._writer.write(bytes(packet))
            await asyncio.sleep(0.5)
